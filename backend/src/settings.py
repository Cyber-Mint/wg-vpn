import os
import logging

import pydantic

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Settings(pydantic.BaseSettings):
    WG_VPN_REGISTRATION_TOKEN: str = os.getenv('WG_VPN_REGISTRATION_TOKEN')
    WG_VPN_ENDPOINT: str = os.getenv('WG_VPN_ENDPOINT')
    WG_VPN_ALLOWED_IPS: str = os.getenv('WG_VPN_ALLOWED_IPS')
    WG_VPN_SERVER_INTERFACE: str = os.getenv('WG_VPN_SERVER_INTERFACE')
    WG_VPN_SERVER_HOST: str = os.getenv("WG_VPN_SERVER_HOST")
    WG_VPN_SERVER_PUBLIC_KEY: str = os.getenv('WG_VPN_SERVER_PUBLIC_KEY')
    WG_VPN_PACKAGE_PATH: str = os.getenv('WG_VPN_PACKAGE_PATH', '/home/$USER/.wireguard')
    PROJECT_VERSION: str = os.getenv('PROJECT_VERSION', '0.9')
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'wg-vpn')


settings = Settings()
