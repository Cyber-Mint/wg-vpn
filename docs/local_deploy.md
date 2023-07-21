# Local Deployment

This technical documentation provides step-by-step instructions for preparing your development environment and deploying a local virtual machine (VM) using Ubuntu 22.04 LTS server image, Ansible, and your favourite hypervisor.

### Prerequisites

Before proceeding with the deployment, ensure you have the following:

- Virtualization software installed (e.g. VirtualBox, VMware)
- Ubuntu 22.04 LTS server image
- SSH-server installed on the virtual machine
- [Ansible](./Install%20Ansible.md) installed on your local development environment

This technical documentation provides instructions for running the playbook locally to deploy and configure the environment on a local virtual machine. Follow the steps below to run the playbook and perform the deployment tasks.

### Running the Playbook for the First Time

Before running the playbook locally, ensure you know the following:

- The target VM's IP address or hostname
- The appropriate user credentials for SSH access
- An ssh key for SSH access

Set the VM user environment variable if you provisioned your Ubuntu 22.04 LTS VM with a different user or wish to use a different user:

```bash
export VM_USER=root
```

* First "ping" to your VM with `ansible-playbook` using the **root** user and SSH key to ensure you are able to correctly connect:

```bash
cd playbook/
ansible -i inventory/local -m ping $VPN_SERVER_NAME --user vagrant --ask-pass
```
This should respond to the "ping" with a "pong" as follows:

 ```text
192.168.122.168 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
 ```

Now, that we know we can reach the local server with `ansible-playbook` correctly.

Before running the playbook ensure that your inventory files `playbook/inventory/local` points to the appropriate IP addresses, such as:

```
[wg_server]
192.168.122.169
```

Enter the root or vagrant password and sudo password when prompted:

```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy-local.yml -i inventory/local -u $VM_USER --ask-pass --ask-become-pass
```

This command will use SSH and sudo access to connect to the target VM and execute the playbook.

> If you have multiple SSH keys, specify the path to your SSH key using the `--key-file` option.

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
[HOME](../README.md) | [Technical Documentation](./README.md)

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](./LICENSE)




### Deployment Steps






3. Copy your public key to the repository:
- Locate your public key file (usually named <name-of-key>.pub).
- Copy the public key to the `playbook/keys` folder in the playbook directory:
```bash
cd playbook/
cp ~/.ssh/<name-of-key>.pub keys/<name-of-key>.pub
```


