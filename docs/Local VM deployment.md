# Local VM Deployment

This technical documentation provides step-by-step instructions for preparing your development environment
and deploying a local virtual machine (VM) using Ubuntu 22.04 LTS server image and Ansible.

### Prerequisites

Before proceeding with the deployment, ensure you have the following:

- A virtualization software installed (e.g., VirtualBox, VMware)
- Ubuntu 22.04 LTS server image
- SSH-server installed on the virtual machine
- Ansible installed on your local development environment

### Deployment Steps

Follow these steps to prepare your development environment and deploy the local VM:

1. Create a virtual machine:

- Create a virtual machine using your preferred virtualization software.
- Select the Ubuntu 22.04 LTS server image.
- During the installation, optionally create a user vagrant with the password vagrant. If not specified, the script
  assumes the user is root.

2. Install Ansible and set up your environment:

- Open a terminal on your local development environment.
- Remove any existing Ansible installation:

```bash
sudo apt purge ansible
```

- Add the Ansible PPA repository and update the package list:

```bash
sudo apt-add-repository ppa:ansible/ansible
sudo apt update -y && sudo apt upgrade -y
```

- Install Ansible and required dependencies:

```bash
sudo apt install ansible python3-argcomplete
sudo activate-global-python-argcomplete3
```
- Verify the installation by checking the Ansible version:

```bash
ansible --version
```
- Ensure that your inventory files (inventory/dev and inventory/prod) point to the appropriate host/IP addresses, such as
`10.0.0.123` or `myvpn.com`.
- Test the Ansible installation by pinging the target host:

```bash
export $VPN_SERVER_NAME=wg_server
cd playbook/
ansible -i inventory/local -m ping $VPN_SERVER_NAME --user vagrant --ask-pass
```
> This command will prompt you for the password and display a success message if the connection is established.

3. Copy your public key to the repository:
- Locate your public key file (usually named <name-of-key>.pub).
- Copy the public key to the `playbook/keys` folder in the playbook directory:
```bash
cd playbook/
cp ~/.ssh/<name-of-key>.pub keys/<name-of-key>.pub
```

By following these steps, you will have prepared your development environment and deployed a local VM using Ubuntu 22.04
LTS server image and Ansible.

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](../LICENSE)
