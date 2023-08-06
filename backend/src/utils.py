import os
import subprocess
import logging

from settings import settings

wireguard_conf_file = '/etc/wireguard/wg0.conf'
lock_file = '/etc/wireguard/add_peer.lock'
peer_db_file = '/etc/wireguard/peers.txt'
peer_indicator = '[peer]'

WG_VPN_SERVER_INTERFACE = settings.WG_VPN_SERVER_INTERFACE

logger = logging.getLogger('uvicorn')


def search_peers(file_path: str) -> str:
    """
    Search for peers in the specified file and determine the next available subnet IP.

    Args:
        file_path (str): Path to the file containing the list of peers.

    Returns:
        str: The next available subnet IP for a new peer.

    Example:
        >>> search_peers("/etc/wireguard/peers.txt")
        '10.0.0.3'
    """
    subnet = WG_VPN_SERVER_INTERFACE.split('.')
    peers = [int(subnet[-1])]
    with open(file_path, 'r') as file:
        for line in file:
            peer = line.rstrip('\n').split(" ")
            if len(peer) != 3 or peer[0] != peer_indicator:
                continue
            if (peer := int(peer[1].split(".")[-1])) not in peers:
                peers.append(peer)
    next_sub_ip = next(iter(set(range(1, 255)) - set(peers)))
    subnet[-1] = str(next_sub_ip)
    return ".".join(subnet)


def determine_next_private_ip() -> str:
    """
    Determine the next available private IP address for a new peer.

    Returns:
        str: The next available private IP address.

    Example:
        >>> determine_next_private_ip()
        '10.0.0.3'
    """
    if not os.path.isfile(peer_db_file):
        command = ["touch", peer_db_file]
        logger.info(f"Executing: {command}")
        subprocess.run(command, shell=True, check=False)
        logger.info(f"Generated new {peer_db_file}")
    return search_peers(peer_db_file)


def generate_key_pair() -> dict:
    """
    Generate a Wireguard key pair consisting of a private key and a corresponding public key.

    Returns:
        dict: A dictionary containing the generated private and public keys.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.

    Example:
        >>> generate_key_pair()
        {'private_key': 'xmrz4MZdFvgWUss6XwZt2T/AOe64E2jTh1lG96V9pC8=',
         'public_key': 'VGsDbHy4OvrgZ8OkX1Y9GmEs+6bQ6MDg8N6DbKAvdLE='}
    """
    private_key = subprocess.run(
        ["wg genkey"], shell=True, capture_output=True, text=True, check=False).stdout.replace('\n', '')
    public_key = subprocess.run(
        [f"echo '{private_key}' | wg pubkey"], shell=True, capture_output=True, text=True,
        check=False).stdout.replace('\n', '')
    return {
        "private_key": private_key,
        "public_key": public_key
    }


def store_client(client_address: str, public_key: str) -> None:
    """
    Store the client information in the peer database file and update the Wireguard configuration.

    Args:
        client_address (str): The client's IP address.
        public_key (str): The client's public key.

    Returns:
        None

    Example:
        >>> store_client("10.0.0.3", "abcdef1234567890")
    """
    command = [f'echo "{peer_indicator} {client_address} {public_key}" | tee -a {peer_db_file}']

    logger.info(f"Executing: {command}")

    subprocess.run(command, shell=True)

    command = [f'echo "wg set wg0 peer {public_key} allowed-ips {client_address}" | tee -a /home/wg-vpn/commandpipe']
    logger.info(f"Executing: {command}")

    subprocess.run(command, shell=True, check=False)

    logger.info(f"Stored client {client_address} in the peer database and updated Wireguard configuration.")


def obtain_lock_file() -> None:
    """
    Obtain the lock file to ensure exclusive access during peer addition.

    Returns:
        None

    Raises:
        ReferenceError: If the lock file already exists.

    Example:
        >>> obtain_lock_file()
    """
    if os.path.isfile(lock_file):
        raise ReferenceError("The add_peer lock file has not been released")

    command = [f'touch {lock_file}']
    logger.info(f"Executing: {command}")

    subprocess.run(command, shell=True, check=False)

    logger.info(f"Obtained the lock file: {lock_file}")


def release_lock_file() -> None:
    """
    Release the lock file to allow other processes to access the resource.

    Returns:
        None

    Raises:
        ReferenceError: If the lock file does not exist.

    Example:
        >>> release_lock_file()
    """
    if not os.path.isfile(lock_file):
        logger.warning("The add_peer lock file does not exist on release")
    else:
        command = [f'rm {lock_file}']
        logger.info(f"Executing: {command}")

        subprocess.run(command, shell=True, check=False)

        logger.info(f"Released the lock file: {lock_file}")


def get_tunnel_ips() -> str:
    """
    Generate a list of IPs to construct encrypted tunnels for.
    This list is interpreted with /bin/sh

    Returns:
        str: A list of IPs, in /bin/sh format.

    Example:
        >>> get_tunnel_ips()
        '1.1.1.1\n2.2.2.2\n3.3.3.3\n4.4.4.4\n5.5.5.5\n'
    """
    allowed_ips = settings.WG_VPN_ALLOWED_IPS.split(',')
    tunnel_ips = '\n'.join(allowed_ips)
    return tunnel_ips + '\n'

