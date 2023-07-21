# Production Deploy


### Setup Procedure for Administrators
- Provision a clean 23.04 or later Ubuntu-based VM in the cloud with only SSH (port 22) root access. 
- Update the server IP in the `playbook/inventory/prod` file.
- Set up a DNS A record for **vpn.my.domain** associated with the server IP address.
- Update the `playbook/inventory/prod` file with the IP address of your server.
- Update the `playbook/vars/prod.yml` file with the following information:
```yaml
vpn_server_name: vpn.my.domain
```

- Export the following environment variables:
```bash
export VPN_VERSION=0.9
export VPN_ALLOWED_IPS=0.0.0.0/0
export VPN_ENDPOINT=vpn.my.domain:51820
export VPN_SERVER_NAME=vpn.my.domain
export VPN_WEBSERVER_EMAIL=info@my.domain.com
export VPN_SERVER_HOST=https://vpn.my.domain
```
> Note: Allowed IPs are the individual IP addresses, comma separated such as `132.23.442.234, 132.233.42.24, 8.8.8.8` or IP subnet masks such as `10.50.0.0/24` or all addresses using `0.0.0.0/0` that clients will access via the VPN.

- [Install `ansible`](./install_ansible.md) and required dependencies for running the playbook. 
- Run the playbook using the instructions below, which will automatically:
  - Harden the VPN server
  - Add a **vagrant** user
  - Install the VPN Admin's SSH public key
  - Remove **root** SSH access
  - Install dependencies
  - Configure `wg-vpn``
  - Add a Let's Encrypt SSL certificate for your **vpn.my.domain**
- The playbook will display a valid registration **`TOKEN`**, which can be provided to users to use when self-registering with the VPN server.

### Running the Playbook on Production

- First "ping" to your VM with `ansible-playbook` using the **root** user and SSH key to ensure you are able to correctly connect:

```bash
cd playbook/
ansible -i inventory/prod -m ping $VPN_SERVER_NAME --user vagrant --ask-pass
```
This should respond to the "ping" with a "pong" as follows:

 ```text
vpn.my.domain | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
 ```
Now, that we know we can reach our production server with `ansible-playbook` correctly, we can go ahead and run the playbook for the first time.

```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy.yml -i inventory/prod -u root --private-key ~/.ssh/id_rsa
```
> This command will execute the playbook using the **root** user and the specified SSH key.



- `deploy-all.yml`: Performs a full deployment and should always be run first.

To run the playbook for subsequent production re-deployment, use the following command:

```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy-all.yml -i inventory/prod -u vagrant
```

### Deployment Alternatives

To run the playbook from a specific task, such as the Docker steps, use the --start-at-task option:

```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy-all.yml -i inventory/prod -u vagrant --start-at-task="docker"
```
<br>

---
[HOME](../README.md) | [Technical Documentation](./README.md)

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](./LICENSE)
