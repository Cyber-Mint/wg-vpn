# Environment variables used in wg-vpn

**VPN_VERSION**:<br>
_Floating point number_<br>
This variable speaks to the release version [on Dockerhub](https://hub.docker.com/r/cybermint/wg-vpn) to which you would
like to use.
> **Note**: You are able to set this value to "latest", and not pin it to a specific version. <br>
> Contributors to this project take care To make this project as backward compatible as possible, but it is still
> recommended to pin your versions

**VPN_ALLOWED_IPS**:<br>
_String_<br>
This variable is for the **vpn peers**. It is set by the system admin, and is the initial list of IPs and Networks for a
peer to tunnel through the VPN to get to.
> **Note**: The documentation default is to set this to "0.0.0.0/0", which would route all of a registered peer's
> traffic through the VPN.<br>
> **Note**: This value is ultimately set by the peer, as peers have the ability to change and control it after
> registration

```bash
export VPN_ENDPOINT=vpn.my.domain:51820
export VPN_SERVER_NAME=vpn.my.domain
export VPN_WEBSERVER_EMAIL=info@my.domain.com
export VPN_SERVER_HOST=https://vpn.my.domain
export VPN_ROTATE_REGISTRATION_TOKEN=<boolean>
```