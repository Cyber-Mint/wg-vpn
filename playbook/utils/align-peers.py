#!/usr/bin/python3
# Copyright (c) 2023, Cyber-Mint (Pty) Ltd
# License MIT: https://opensource.org/licenses/MIT

import subprocess

peer_db_file = '/etc/wireguard/peers.txt'
peer_indicator = '[peer]'


def configure_wireguard_peer(client_address: str, public_key: str) -> None:
    """
    Configures a WireGuard peer on the host server.
    Args:
        client_address: The client's IP address.
        public_key: The public key of the client.
    """
    command = ['sudo', 'wg', 'set', 'wg0', 'peer', public_key, 'allowed-ips', client_address]
    subprocess.run(command)


if __name__ == '__main__':
    # Dictionary to store known peers
    known_peers = {}

    # Get the output of the 'sudo wg' command and extract the known peers
    command_output = subprocess.run(['sudo', 'wg'], capture_output=True, text=True)
    for known_peer in command_output.stdout.replace('\n', '').split('peer: ')[1:]:
        _, allowed_ips = known_peer.split('  allowed ips: ')
        known_peers[allowed_ips.split('/')[0]] = _

    # Open the peer database file
    with open(peer_db_file, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            peer = line.rstrip('\n').split(" ")
            # Skip if the line is ill-constructed or doesn't match the indicator
            if len(peer) != 3 or peer[0] != peer_indicator:
                continue
            # Add the peer to the host if it's not already a known peer
            if peer[1] not in known_peers:
                configure_wireguard_peer(client_address=peer[1], public_key=peer[2])
