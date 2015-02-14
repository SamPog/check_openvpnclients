#! /usr/bin/python3

# Check if an OpenVPN server runs with the management interface
# and displays the list of clients connected to the VPN.
#
# The management interface must be enabled, in your server configuration file
# add the line in your server.cfg and reload your server :
# management [IP NETWORK] [PORT QUERY]
# ex : management 0.0.0.0 7505
#
# check_openvpnclients.py -H HOSTADDRESS -p QUERYPORT [-D html|default]


import telnetlib
import sys
import argparse
import socket
import time

arguments = dict()
return_codes = {'OK': 0,
                'WARNING': 1,
                'CRITICAL': 2,
                'UNKNOWN': 3 }

def argsread():
    """
    LECTURE DES ARGUMENTS
    """
    parser = argparse.ArgumentParser(description="Check OpenVPN")
    parser.add_argument('-H', '--host', type=str, default="", help="OpenVPN server address")
    parser.add_argument('-p', '--port', type=str, default="7505", help="Port management interface")
    parser.add_argument('-D', '--display', type=str, default="default", help="Display type : default or html")
    args = parser.parse_args()
    if args.host=="":
        print("The host address is not specified")
        sys.exit(return_codes['UNKNOWN'])
    global arguments
    arguments["serverAddress"] =    args.host
    arguments["queryport"] = args.port
    arguments["displayType"] = args.display
    
def telnet_request():
    """
    CONNEXION AU SERVEUR TS
    """
    try:
        tn = telnetlib.Telnet(arguments["serverAddress"], arguments["queryport"])
    except:
        print("Error ! Failed to connect to query port. ", end='')
        print("Verify that the management interface is enabled on port {0} or specify another port with the parameter --qport".format(arguments["queryport"]))
        sys.exit(return_codes['UNKNOWN'])
    tn.write(b"status \n")
    time.sleep(0.5)
    tn.write(b"exit \n")
    tn.read_until(str.encode("Since\r\n"))
    reponse = tn.read_until(str.encode("\r\nROUTING TABLE"))
    tn.close()
    return reponse

def processing(clientlist): 
    """
    TRAITEMENT
    """
    clientlist = clientlist.decode('utf8').rstrip('\r\nROUTING TABLE')
    tabl_resultat = clientlist.split('\n')
    resultat = ""
    i=0
    for ligne in tabl_resultat:
        tabl_resultat[i] = ligne.split(',')[0]
        i+=1
    return tabl_resultat
    
def default_print(tablReponse):
    """
    SORTIE STANDARD 
    """
    if len(tablReponse) == 0:
        print("Aucun client connecté.")
    elif len(tablReponse) == 1:
        print(" {0} client connected :".format(len(tablReponse)), end=' ')
    else:
        print(" {0} clients connected :".format(len(tablReponse)), end=' ')
    for client in tablReponse:
        print(client, end=', ')
    print("| clients=" + str(len(tablReponse)))

def html_print(tablReponse):
    """
    SORTIE HTML
    """
    if len(tablReponse) == 0:
        print("Aucun client connecté.")
    elif len(tablReponse) == 1:
        print(" {0} client connected :".format(len(tablReponse)), end=' ')
    else:
        print(" {0} clients connected :".format(len(tablReponse)), end=' ')
    print("<ul>", end='')
    for client in tablReponse:
        print("<li>" + client + "</li>", end='')
    print("</ul>| clients=" + str(len(tablReponse)))

def main():
    """
     MAIN
    """ 
    argsread()
    if arguments["displayType"]=="default":
        default_print(processing(telnet_request()))
    elif arguments["displayType"]=="html":
        html_print(processing(telnet_request()))
    sys.exit(return_codes['OK'])
    
# Main program
##############
if __name__ == "__main__":
    main();

