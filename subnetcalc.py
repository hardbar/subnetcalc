#!/usr/bin/python3
"""
Created on Tue Aug 29 16:06:02 2017

@author: barry
Description: Get an IP address and subnet mask, return detailed host and subnet information    
As an Example: 192.168.0.1/24 will print the following information:

IP host information:
Address:     192.168.0.1           11000000.10101000.00000000 .00000001
Netmask:     255.255.255.0         11111111.11111111.11111111 .00000000
Wildcard:    0.0.0.255             00000000.00000000.00000000 .11111111

IP Subnet information:
Network:     192.168.0.0/24        11000000.10101000.00000000 .00000000
Broadcast:   192.168.0.255         11000000.10101000.00000000 .11111111
FirstHost:   192.168.0.1           11000000.10101000.00000000 .00000001
LastHost:    192.168.0.254         11000000.10101000.00000000 .11111110
AvailHosts:  254

@version: 0.1  -01/09/2017 finished coding the basic functionality - cmd line only

"""
##
# ****all imports****
##

import re
import ipaddress

##
# ****version info****
##
version = "v0.1"
buildDate = "01/09/2017"

##
# ****global variables****
##

# use regex to verify IP is valid
checkInput = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

##
# ****ALL FUNCTIONS UNDER HERE****
##

# check to make sure user enters a valid ip address
def userInput(ip):
    """ Uses ipaddress module to verify a valid IP is given
        Print an error message if it is invalid and prompt user to re-enter

        Keyword arguments:
        ip -- ip address or "Q" to quit, entered by user
    """
    while True:
        try:
            if str.lower(str(ip)) == "q":
                return print("Goodbye!\n")
            if ipaddress.ip_interface(ip) != ValueError:
                print("Valid IP/prefix ...\n")
                return ip
        except ValueError:
            print("\nThis is an invalid address/prefix: ", ip)
            ip = input("Enter an IP and prefix mask, or Q to quit: ")

    
# prints out detailed information about user provided input
def ipDetail(ip):
    """ Uses ipaddress module to display information about the user entered IP and mask

        Keyword arguments:
        ip -- ip address entered by user
    """    
    ipInt = ipaddress.ip_interface(ip)    # object to extract 
    ipNet = ipInt.network    # object to extract subnet host is on and to obtain the netmask
    ipNetwork = ipaddress.ip_network(ip, strict=False)    # object to extract 
    template = "{0:14}{1:18}{2:40}" # set column widths: 14, 18, 40
    template1 = "{0:14}{1:18}" # set column widths: 14, 18
    
# all host information provided below
    print("IP host information:")

# print the given ip address and its binary equivalent
    ipOnly = ip.split('/')
    ipBinary = '.' .join(format(int(i), "08b") for i in ipOnly[0].split("."))
    print(template.format("Address:", ipOnly[0], ipBinary))

# print out the netmask and its binary equivalent
    netmaskBinary = '.' .join(format(int(i), "08b") for i in (str(ipNet.netmask)).split("."))
    print(template.format("Netmask:", str(ipNet.netmask), netmaskBinary))    

# print out the wildcard mask and its binary equivalent
    hostmaskBinary = '.' .join(format(int(i), "08b") for i in (str(ipNet.hostmask)).split("."))
    print(template.format("Hostmask:", str(ipNet.hostmask), hostmaskBinary))

# all subnet information provided below
    print("\nIP Subnet information:")

# print out the network and its binary equivalent
    ipnetOnly = str(ipNet).split("/")
    subnetBinary = '.' .join(format(int(i), "08b") for i in (str(ipnetOnly[0])).split("."))
    print(template.format("Network:", str(ipNet), subnetBinary))

# print out the broadcast and its binary equivalent
    bcastBinary = '.' .join(format(int(i), "08b") for i in (str(ipInt.network.broadcast_address)).split("."))
    print(template.format("Broadcast:", str(ipInt.network.broadcast_address), bcastBinary))

# print out the first host and its binary equivalent
    firstHost = ipNetwork[1]
    firstHostBinary = '.' .join(format(int(i), "08b") for i in str(firstHost).split("."))
    print(template.format("FirstHost:", str(firstHost), firstHostBinary))

# print out the last host and its binary equivalent
    lastHost = ipNetwork[-2]
    lastHostBinary = '.' .join(format(int(i), "08b") for i in str(lastHost).split("."))
    print(template.format("LastHost:", str(lastHost), lastHostBinary))

# print out the number of hosts on the subnet
    availHosts = int(lastHost) - int(firstHost)
    print(template1.format("AvailHosts:", str(availHosts)))
    print()

##
# ****MAIN****
##
def main():
    """
    This is the main function for the subnetcalc.py program
    This module represents the (otherwise anonymous) scope in which the interpreter’s main 
    program executes — commands read either from standard input, from a script file, or from an interactive prompt.
    """
    print("\n***This tool is a subnet calculator that will provide IP and subnet information***")
    print("subnetcalc.py version " + version +  " build date " + buildDate)
    print("Usage: Specify a valid host/network IP address with prefix mask in the format 'x.x.x.x/x'\n")

# get input from user and check if valid
    userIP = input("Enter an IP and prefix mask, or Q to quit: ")

# verify that a valid IP has been entered
    userIP = userInput(userIP)

# calculate and display information about the given IP/prefix
    if userIP == None:
        exit(1)             # use exit(1) to exit the program, any value other than 0 can be used here
    else:
        ipDetail(userIP)


if __name__ == "__main__":
    main()