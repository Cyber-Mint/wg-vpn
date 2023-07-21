# Running the Playbook Locally

This technical documentation provides instructions for running the playbook locally to deploy and configure the environment. Follow the steps below to run the playbook and perform the
deployment tasks.

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

### Running the Playbook on Production

Assuming a new VM has been provisioned on DigitalOcean (use your cloud provider of choice), follow these steps to run the playbook on production:

Log in to the VM using the root user and SSH key:
```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy.yml -i inventory/prod -u root --private-key ~/.ssh/id_rsa
```
> This command will execute the playbook using the root user and the specified SSH key.

By following these steps, you can run the playbook locally and perform the necessary deployment tasks. Ensure you have the required credentials and access permissions to execute the playbook successfully.

- `deploy-all.yml`: Performs a full deployment and should always be run first.

To run the playbook for subsequent production re-deployment, use the following command:

```bash
ANSIBLE_NOCOWS=1 ansible-playbook deploy-all.yml -i inventory/prod -u vagrant
```

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](../LICENSE)
