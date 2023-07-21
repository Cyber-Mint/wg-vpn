# BE Service

## Overview

The BE Service is a Python BackEnd service implemented using the FastAPI framework.
Its main responsibilities include managing a 'peers database' text file, registering
VPN peers to the server's WireGuard configuration, and generating peer 'install.sh' scripts
for installing a command-line VPN controller.

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/):  A modern, fast (high-performance), web framework
- for building APIs with Python.

## Functionality

### Managing a 'peers database' text file

The BE Service utilizes a 'peers database' text file to store information about registered peers.
This file maintains records of peer public keys and the assigned private IP ranges.
During server redeployment, the peers' information is wiped and re-added from the 'peers.txt' file.
Successful peer registrations result in the addition of the new peer's public key and private IP to this file.

### Registering VPN peers to the server's WireGuard configuration

The BE Service facilitates the registration of VPN peers to the server's WireGuard configuration.
This process involves adding peer details, such as the public key and private IP,
to the server's WireGuard configuration file. By registering VPN peers, the server can establish
secure connections with these peers.

### Generating peer 'install.sh' scripts

The BE Service generates 'install.sh' scripts specifically tailored for individual peers.
These scripts enable the installation of a command-line VPN controller on the peer's device.
By executing the 'install.sh' script, peers can conveniently set up and configure the VPN controller
to establish a secure connection with the server.

### Testing registering a peer

To test the registration of a peer, follow these steps:

- Set the following environment variable:

```bash
$ export WG_VPN_REGISTRATION_TOKEN='test_token8243dgdGd'
```

- Navigate to the 'backend/' directory.
- Start the BE Service using Docker Compose:

```bash
docker-compose up -d
```

- Register the peer by sending a GET request to the '/generate' endpoint with the registration token:

```bash
curl -s -L http://127.0.0.1:8000/generate?token=${WG_VPN_REGISTRATION_TOKEN}
```

- Retrieve the 'installer.sh' script by sending a GET request to the '/register' endpoint with the registration token
  and save it as 'installer.sh':

```bash
curl -s -L http://127.0.0.1:8000/register?token=${WG_VPN_REGISTRATION_TOKEN} -o installer.sh
```

- Run the 'installer.sh' script to install the CLI VPN controller on the peer's device:

```bash
bash installer.sh 
```

### Peer 'database' file

The BE Service relies on a 'peers database' text file to store information about known peers.
Here are the key details regarding this file:

- The file stores records of peer public keys and the assigned private IP ranges.
- During server redeployment, the peers' information is wiped, and the file is used to re-populate the server's peers.
- Successful peer registrations result in the storage of the new peer's public key and private IP in this file.

> **Note**: The actual implementation details and specific configurations may vary based on the
> underlying system and deployment environment.
