[![CircleCI](https://dl.circleci.com/status-badge/img/gh/Cyber-Mint/wg-vpn/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/Cyber-Mint/wg-vpn/tree/master)

# Wireguard VPN

Wireguard VPN is an ultra-light implementation of a simplified configuration service for Wireguard deployments, 
designed for use with Linux clients.

### Overview
> **References**: Digital-Ocean Wireguard [tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-wireguard-on-ubuntu-22-04)

[Wireguard](https://www.wireguard.com/) is a lightweight, fast, secure, and relatively new Virtual Private Network (VPN), that supports IPv4 and IPv6 connections. The encryption in WireGuard works by utilizing public and private keys to establish an encrypted "tunnel".

---

## Administrator Documentation

The Wireguard VPN service is deployable by an administrator to any VM cloud instance using an Ansible playbook. 
It serves as a great companion to the wg-quick script and wg VPN.

**Deployment Topology**
The following diagram illustrates the typical deployment topology:
![wg-vpn](./docs/wg-vpn.png)

**Setup Procedure for Administrators**
- Provision a clean Ubuntu-based VM in the cloud with only SSH (port 22) root access. Update the server IP in the playbook/inventory/prod file.
- Set up a DNS A record for vpn.my.domain associated with the server IP address.
- Update the playbook/inventory/prod file with the IP address of your server
- Update the playbook/vars/prod.yml file with the following information:
```yaml
vpn_server_name: vpn.my.domain
```
- Export the following environment variables:
```bash
export VPN_VERSION=0.9
export VPN_ALLOWED_IPS=0.0.0.0/24  # or a comma separated list e.g. VPN_ALLOWED_IPS=132.23.442.234, 132.233.42.24, 8.8.8.8
export VPN_ENDPOINT=vpn.my.domain:51820
export VPN_SERVER_NAME=vpn.my.domain
export VPN_WEBSERVER_EMAIL=info@my.domain.com
export VPN_SERVER_HOST=https://vpn.my.domain
```
> Note: Allowed IPs are the individual IP addresses or IP ranges that clients will access via the VPN.
- Run the playbook, which will automatically:
  - Harden the VPN server
  - Add a vagrant user
  - Install the administrator's SSH public key
  - Remove root SSH access
  - Install dependencies
  - Configure wg-vpn
  - Add a Let's Encrypt SSL certificate
- The playbook will display a valid registration token $TOKEN, which can be provided to users when self-registering with the VPN server.

## Client Documentation

The Wireguard VPN service allows users (also known as peers) to self-register and configure their client instances of wg to make use of the VPN.
Setup Procedure for Clients
- Users can self-register by visiting https://vpn.my.domain and providing the registration token in the following URL format: https://vpn.my.domain/register?token=$TOKEN.
- The website will generate a command for the client to use and install the wg-vpn cli. 
- To register with the vpn without going through the Front End, use the below command:
```bash
curl -sSL -H "Authorization: Bearer $TOKEN" https://vpn.my.domain/register -o wg-vpn-installer.sh && bash wg-vpn-installer.sh
```
> This will install the necessary dependencies, wg and wg-quick, and configure the wg0.conf file. 
> The VPN will be tethered to vpn.my.domain.
- After executing the script, users can see the capabilities of the application by executing `wg-vpn --help`:<br>
```bash
Usage wg-vpn [COMMAND].. [OPTION]
   wg-vpn is a WireGuard wrapper to easily run a peer with a wg-vpn server

  [COMMAND]:
    up,UP           bring the peer VPN connection up
    down,DOWN       bring the peer VPN connection down
    uninstall       uninstall wg-vpn

  [OPTION]:
    -q, --quiet     produces no terminal output,
                    except setting bash return value \$? = 1 if failures found.
        --version   display the version and exit
        --help      display this help and exit


  EXAMPLE(s):
      wg-vpn up -q
      wg-vpn down
      wg-vpn status
```

### Client Uninstalling

To remove the client installation simply executing `wg-vpn uninstall` which will remove the application and the local user specific `wg0.conf` file.
<br>

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](./LICENSE)

