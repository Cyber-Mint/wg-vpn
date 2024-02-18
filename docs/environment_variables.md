# Environment variables used in wg-vpn

**VPN_ROTATE_REGISTRATION_TOKEN**:<br>
_Boolean_<br>
This variable determines if you want to persist for same registration token through different deployments, 
or generate a new token after each deployment.

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

**VPN_ENDPOINT**:<br>
_String (IP:port)_<br>
This variable is used by the backend service when generating a wg0.conf templated file. This is set as the peer's endpoint
for tunnel traffic through the server

**VPN_SERVER_HOST**:<br>
_String (proto://IP)_<br>
This variable is used for generating the redirect on the FE page. i.e. After the FE validates a request with the registration
token, and returns a cURL to download the wg0 config, this is the host that will provide the static asset for downloading.

**VPN_SERVER_NAME & VPN_WEBSERVER_EMAIL**:<br>
_String_<br>
These variables are used by the NGINX role. `VPN_SERVER_NAME` is the domain name of your WG-VPN server, 
and `VPN_WEBSERVER_EMAIL` is your administrator's email address.
