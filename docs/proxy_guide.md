# Nginx Reverse Proxy Configuration for VPN Access

To enhance security, it is recommended to configure an Nginx reverse proxy to only accept connections
from the Wireguard VPN. This ensures that only authorized VPN users can access the protected resources
served by Nginx.

### Prerequisites

Before proceeding with the configuration, make sure you have the following:

- A running Nginx server
- A working server, deployed using this repo's playbook
- The public IP address of the Wireguard VPN server (<vpn_public_ip> in the example code)

### Configuration Steps

Follow these steps to set up the Nginx reverse proxy to only accept connections from the Wireguard VPN:

- Open the Nginx configuration file in a text editor. The file is typically located at /etc/nginx/nginx.conf or within
  the /etc/nginx/conf.d/ directory.
- Locate the server block that corresponds to the virtual host or website you want to protect with the Wireguard VPN.
- Within the server block, add the following code snippet:

```nginx
location / {
    allow      <vpn_public_ip>;
    deny       all;
    # Your other proxy directives go here
    proxy_pass http://backend_server;
}
```

Replace `<vpn_public_ip>` with the public IP address of your Wireguard VPN server. This configuration restricts access
to
only requests originating from the VPN. Incoming requests from other IP addresses will be denied.

- Save the Nginx configuration file and exit the text editor.
- Test the Nginx configuration for syntax errors:

```bash
sudo nginx -t
```

If there are no errors, proceed to the next step. Otherwise, review your configuration for any mistakes.
- Restart Nginx to apply the changes:
```bash
sudo systemctl restart nginx
```
- Verify that Nginx is accepting connections only from the Wireguard VPN by attempting to access the protected website or resource from a non-VPN network. Access should be denied.
- Connect to the Wireguard VPN and attempt to access the protected website or resource again. Access should now be granted.

### Additional Considerations
- By using the allow and deny directives in the Nginx configuration, packets from unauthorized IP addresses will be dropped at the Nginx level, providing an additional layer of security.
- It is important to note that dropping packets on the client side is a serious action and should be approached with caution. Dropping packets on the client side may result in loss of network connectivity or unintended consequences. It is recommended to implement packet filtering or firewall rules on the server-side or network infrastructure to enforce access restrictions.
- Make sure to update the Nginx configuration for each website or virtual host that you want to protect with the Wireguard VPN.
- Consider adding SSL/TLS encryption to the Nginx reverse proxy configuration to ensure secure communication between the VPN clients and the protected resources.
- Regularly monitor Nginx logs and access attempts to ensure the security of your system.

By following these steps and dropping packets at the Nginx level, you can enhance the security of your Nginx server and
ensure that only authorized VPN users can access the protected resources.

<br>

---
[HOME](../README.md) | [Technical Documentation](./README.md)

---
Copyright &copy; 2023, Cyber-Mint (Pty) Ltd<br>
Supplied under [MIT License](./LICENSE)
