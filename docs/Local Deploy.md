# Local Deploy

This technical documentation provides instructions for running the playbook locally to deploy and configure the environment on a local virtual machine. Follow the steps below to run the playbook and perform the deployment tasks.

### Prerequisites

Before running the playbook locally, ensure you have the following:

- The target VM's IP address or hostname
- SSH access to the target VM
- The appropriate user credentials for SSH access

### Running the Playbook for the First Time

When running the playbook for the first time, follow these steps:

1. Set the VM user environment variable if you provisioned your Ubuntu 22.04 LTS VM with a different user or wish to use a different user:

```bash
export VM_USER=root
```

2. Enter the root or vagrant password and sudo password when prompted:

```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy-local.yml -i inventory/local -u $VM_USER --ask-pass --ask-become-pass
```

> This command will use SSH and sudo access to connect to the target VM and execute the playbook.

3. If you have multiple SSH keys, specify the path to your SSH key using the --key-file option.

### Subsequent Playbook Runs

For subsequent playbook runs, use the following command:

```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy-local.yml -i inventory/local -u vagrant
```

This command will use your SSH key for authentication and sudo access, without prompting for passwords.

### Deployment Alternatives

To run the playbook from a specific task, such as the Docker steps, use the --start-at-task option:

```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy-local.yml -i inventory/local -u vagrant --start-at-task="docker"
```

<br>

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](../LICENSE)


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
