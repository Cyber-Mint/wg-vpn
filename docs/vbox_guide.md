# Virtual Box Guide

To properly configure Virtual Box on Ubuntu, you will need to:
- Download & install Virtual Box & Virtual Box Extensions
- DOwnload & install the latest Ubuntu server `.iso` file
- Add the aptitude package
- Add the repo's gpg keys to your trusted gpg keys folder
- Add a bridge network Adaptor for communicating to your VM via ssh

> **Note**: [here](https://ubuntu.com/download/server) is where to download the latest Ubuntu live server `.iso` file


## Installing VirtualBox

<br>

### Preparing your system

We always recommend you run latest stable versions of your installed packages. If you don’t want to upgrade any package,
just update APT package index and skip the upgrade.

```bash
$ sudo apt update && sudo apt -y upgrade
$ [ -f /var/run/reboot-required ] && sudo reboot -f
```

### Import Virtual Box GPG Keys

Add repository key as follows:

```bash
#Download
$ curl https://www.virtualbox.org/download/oracle_vbox_2016.asc | gpg --dearmor > oracle_vbox_2016.gpg
$ curl https://www.virtualbox.org/download/oracle_vbox.asc | gpg --dearmor > oracle_vbox.gpg

#Install on system
$ sudo install -o root -g root -m 644 oracle_vbox_2016.gpg /etc/apt/trusted.gpg.d/
$ sudo install -o root -g root -m 644 oracle_vbox.gpg /etc/apt/trusted.gpg.d/
```

### Add VirtualBox 7.0 Repository

Once the system is updated and the repository key imported, you can add the VirtualBox Repository by running the commands
below:

```bash
$ echo "deb [arch=amd64] http://download.virtualbox.org/virtualbox/debian $(lsb_release -sc) contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list
```

### Install VirtualBox 7.0 & Extension pack

Finally, install VirtualBox on your Ubuntu 22.04|20.04|18.04 system by running the commands:

```bash
$ sudo apt update
$ sudo apt install linux-headers-$(uname -r) dkms
$ sudo apt install virtualbox-7.0
```

_Download VirtualBox Extension Pack._

```bash
$ cd ~/
$ VER=$(curl -s https://download.virtualbox.org/virtualbox/LATEST.TXT)
$ wget https://download.virtualbox.org/virtualbox/$VER/Oracle_VM_VirtualBox_Extension_Pack-$VER.vbox-extpack
$ sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack
```

Reference used: [install-virtualbox-on-ubuntu-linux](https://computingforgeeks.com/install-virtualbox-on-ubuntu-linux/)

---

### Setup Bridge adaptor

The simplest way to add a bridge network is with `bridge-utils`. To install this package, run:

```bash
$ apt-get install bridge-utils
```

<!-- You can then use the network-manager applet to add a bridge adaptor
```bash
$ nm-applet
```
![Run Applet](Run%20nm%20applet.png)

In the applet, then:
- Create a new wired connection (Ethernet), and name it `DVDK`
- Add the following information to the connection:
<br>
![Edit DVDK](DVDK%20connection.png) -->
> **TO DO**: Give cli instructions for adding a new bridge adapator

<br>

---
[HOME](../README.md) | [Technical Documentation](./README.md)

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](../LICENSE)