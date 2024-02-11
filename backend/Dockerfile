# Build from Python 3.10
FROM python:3.12-alpine

# Set working directory to /code/
WORKDIR /code

# Grant root privileges to the user
USER root

RUN apk add wireguard-tools
RUN apk add curl

# Install requirements
COPY src/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy over chrome_manager and logging config
COPY src /code/

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]

HEALTHCHECK CMD curl --fail http://127.0.0.1:8000/ || exit 1
