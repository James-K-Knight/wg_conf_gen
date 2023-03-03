# Wireguard conf generator

This tool generates a Wireguard configuration file for a peer to connect to an existing host. It is designed to streamline the process of generating configs for client devices to connect to a Pfsense firewall.

## Usage

Copy the config.yaml.dist file to config.yaml and modify the settings to match the required configuration. If the user does not supply arguments, they will be prompted to enter the client interface IP address and the Pre-shared key.

```
usage: run.py [-h] [-l LOG_LEVEL] [-q] [-c CONFIG_FILE] [-ip IP_ADDRESS] [-k PRESHAREDKEY]

options:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Valid loglevels: CRITICAL, ERROR, WARNING, INFO, DEBUG
  -q, --quiet           Disable logging output
  -c CONFIG_FILE        Specify a different config file
  -ip IP_ADDRESS        The interface IP address for the generated conf file
  -k PRESHAREDKEY, --PreSharedKey PRESHAREDKEY
                        Pre-shared key for the generated conf file
```

### Example config:
Note: The private/public keys shown here are not valid keys

Suppose there is a Pfsense firewall with the following Wireguard settings:
```
Listen port: 51820
Interface Keys: 
    Private key for this tunnel: iLaLgk6F58wV875e2s7n3kdyuOIdV/YUo3W53eMkpGs= 
    Public key for this tunnel: wax7iHHdngAPVCQXjgkBd1bAbc88OdxYOQLbzajR5ys=

Interface Configuration (tun_wg0):
    General Configuration:
        IPv4 Configuration Type: Static IPv4
        IPv6 Configuration Type: None
        MTU: 1420
    Static IPv4 Configuration:
        IPv4 Address: 10.10.10.1
```

The resulting config config.yaml would be like so:

```yaml
Interface:
  DNS: 10.10.10.1
  MTU: 1420
Peer:
  AllowedIPs: 10.10.10.1/32, 192.168.0.0/24
  Endpoint: vpn.example.tld:51820
  PublicKey: wax7iHHdngAPVCQXjgkBd1bAbc88OdxYOQLbzajR5ys=
```

Enter the create a new peer interface in Pfsense, generate a new pre-shared key, and then run the script. Enter the output public key into the Pfsense new peer interface.

```cmd
Working Please wait...
Enter Interface IP [Exit]: 10.10.10.2
Enter PreSharedKey [Exit]: vIen+BdTt4tCjAQxE3eX/ERb3g2SIR4iVhW62WkSpSI=
2023-03-03 15:30:05,922 INFO: Generating keys
2023-03-03 15:30:05,957 INFO: Public key: M56PcIRE2jAVoui/fRCr4w8aK5zgtz5u5mhCweT81Ww=
2023-03-03 15:30:05,957 INFO: Output to: 55e9ebebdaa34ba4acfbac4befca68ef.conf
Press any key to continue . . .
```

The output directory will contain a .conf file that can be imported into the client device. The file will have the following format.

```
[Interface]
Address = 10.10.10.2/24
DNS = 10.10.10.1
MTU = 1420
PrivateKey = sOTLfUq0dd6CJ888oOEpT6ExTy0Qi4+SJ/XFS0fn53A=

[Peer]
AllowedIPs = 10.10.10.1/32, 192.168.0.0/24
Endpoint = vpn.example.tld:51820
PreSharedKey = vIen+BdTt4tCjAQxE3eX/ERb3g2SIR4iVhW62WkSpSI=
PublicKey = wax7iHHdngAPVCQXjgkBd1bAbc88OdxYOQLbzajR5ys=
```
