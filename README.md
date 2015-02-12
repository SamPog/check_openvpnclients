**Check_openvpnclients**
====================

 **Plugin for Nagios or Shinken which displays clients connected to OpenVPN**.

Check if an OpenVPN server runs with the management interface and displays the list of clients connected to the VPN.

**The management interface must be enabled**, in your server configuration file add this line in your server.cfg and reload your server : 
management [IP NETWORK] [PORT QUERY]
ex : management 0.0.0.0 7505


Usage :
----------
check_openvpnclients.py -H HOSTADDRESS -p QUERYPORT [-D html|default]
ex : check_openvpnclients.py -H 172.25.5.23 -p 7505 -D html
