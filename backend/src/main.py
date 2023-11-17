import logging
from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from settings import settings

from utils import (
    determine_next_private_ip, generate_key_pair, store_client, obtain_lock_file, release_lock_file, get_tunnel_ips
)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.mount("/static", StaticFiles(directory="static"), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

logger = logging.getLogger('uvicorn')


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    """
    Endpoint to render the index.html template.

    Args:
        request: The incoming request object.

    Returns:
        TemplateResponse: A template response rendering the index.html template.

    """
    return templates.TemplateResponse(
        "index.html", context={"request": request, "host": settings.WG_VPN_SERVER_HOST}
    )


@app.get("/generate", response_class=FileResponse)
async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Endpoint to generate the installer script for VPN registration.

    Args:
        token: The access token for verification.

    Returns:
        JSONResponse: A JSON response containing the detail of the installation command.

    Raises:
        HTTPException: If the provided token is incorrect.

    """
    server_token = settings.WG_VPN_REGISTRATION_TOKEN
    server_host = settings.WG_VPN_SERVER_HOST

    if token != server_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Token provided"
        )

    installer = "wg-vpn-installer.sh"
    detail = (
        f'curl -sSL -H "Authorization: Bearer {server_token}" '
        f'{server_host}/register -o {installer} && bash {installer}'
    )

    return JSONResponse({"detail": detail}, status_code=200)


@app.get("/register", response_class=FileResponse)
async def register(request: Request, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Endpoint to handle the registration process for VPN clients.

    Args:
        request: The incoming request object.
        token: The registration token provided by the client.

    Returns:
        TemplateResponse: A template response rendering the register.sh script.

    """
    server_token = settings.WG_VPN_REGISTRATION_TOKEN

    # Validate the registration token
    if token != server_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Token provided"
        )

    try:
        obtain_lock_file()

        # Generate client address and key pair
        client_address = determine_next_private_ip()
        keys = generate_key_pair()

        # Store client information in the peer database
        store_client(client_address=client_address, public_key=keys.get("public_key"))

        # Prepare the context for the register.sh script
        context = {
            "request": request,
            "client_address": client_address,
            "private_key": keys.get("private_key"),
            "public_key": keys.get("public_key"),
            "endpoint": settings.WG_VPN_ENDPOINT,
            "server_public_key": settings.WG_VPN_SERVER_PUBLIC_KEY,
            "allowed_ips": settings.WG_VPN_ALLOWED_IPS,
            "wireguard_package_path": settings.WG_VPN_PACKAGE_PATH,
            "initial_tunnels": get_tunnel_ips(),
            "wireguard_package_version": settings.PROJECT_VERSION,
        }

        release_lock_file()

        return templates.TemplateResponse("register.sh", context=context)

    except FileNotFoundError as e:
        logger.warning(e)
        release_lock_file()
        return JSONResponse({"error": "There was an error with the server's config"}, status_code=424)

    except ReferenceError as e:
        logger.warning(e)
        return JSONResponse({"error": str(e)}, status_code=423)

    except StopIteration:
        logger.error("Server out of subranges")
        release_lock_file()
        return JSONResponse({"error": "An unexpected error occurred. Contact a maintainer"}, status_code=406)

    except Exception as e:
        logger.error(e)
        release_lock_file()
        return JSONResponse({"error": "An unexpected error occurred"}, status_code=406)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Wireguard API swagger documentation",
        version="2.5.0",
        description="This collection of APIs is for wg-VPN",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    """
    Exception handler for HTTPException.

    Args:
        request: The incoming request object.
        exc: The raised HTTPException.

    Returns:
        TemplateResponse: A template response rendering the error message with the appropriate headers and status code.

    """
    headers = getattr(exc, "headers", None)
    return templates.TemplateResponse(
        "400_error_message.html", context={"request": request}, headers=headers, status_code=exc.status_code
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Exception handler for RequestValidationError.

    Args:
        request: The incoming request object.
        exc: The raised RequestValidationError.

    Returns:
        TemplateResponse: A template response rendering the error message with the appropriate headers.

    """
    headers = getattr(exc, "headers", None)
    return templates.TemplateResponse(
        "400_error_message.html", context={"request": request}, headers=headers
    )
