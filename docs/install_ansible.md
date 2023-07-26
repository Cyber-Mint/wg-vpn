# Install Ansible & Dependencies

- If you are unsure or have any trouble with running the playbook rather remove any existing Ansible installation, and re-install:

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

ansible [core 2.12.10]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/$USER/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /home/$USER/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, May 26 2023, 14:05:08) [GCC 9.4.0]
  jinja version = 3.1.2
  libyaml = True
```

<br>

---
[HOME](../README.md) | [Technical Documentation](./README.md)

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](../LICENSE)
