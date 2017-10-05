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

Flask App Variable/s:
export FLASK_APP=subnetcalc_app.py
export FLASK_DEBUG=1

@version: 0.1  -01/09/2017 finished coding the basic functionality - cmd line only
@version: 0.2  -04/09/2017 added flask to build tool as web app
@version: 0.3  -11/09/2017 completed most of index.html, added some form validation 
@version: 0.4  -13/09/2017 completed layout and design, fixed reset button issue, fixed error handling issues
@version: 0.5  -05/19/2017 fixed bug-id001 :IndexError occurs when user input is only host IP (no mask or /), added if statement to match only if not a host/32 where errors occured
               -05/19/2017 fixed bug-id002 :only first octet of the IP address's binary was displayed, changed "ipOnly[0].split to ipOnly.split" to resolve the issue
               -05/10/2017 added autofocus to input class in index.html
               
TODO
perhaps for version 1.0:
--add whois lookup functionality - see dnspython
--https://stackoverflow.com/questions/24580373/how-to-get-whois-info-by-ip-in-python-3
--a traceroute/ping option

"""
##
# ALL IMPORTS
##

import re
import ipaddress
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import gettempdir


##
# VERSION INFO
##
version = "v0.5"
buildDate = "05/10/2017"

##
# FLASK CONFIGS
##

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


##
# GLOBAL VARIABLES
##

# use regex to verify IP is valid
checkInput = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

##
# ALL FLASK ROUTES UNDER HERE
##

@app.route("/",  methods=["GET", "POST"])
def index():

    # forget any user_id
    session.clear()
    
    # if user reached route via GET
    if request.method == "GET":
        return render_template("index.html")
    
    error = None
    # test for input errors, if none, use lookup to find stock and return price    
    if request.method == "POST":
        if request.form.get("userIP") == "" or request.form.get("userIP") == None:
            error = "Invalid entry, please try again!"
            return render_template("index.html", error=error)
        else:
            pass

    # verify IP entered is a valid IP
    userIP = request.form.get("userIP")
    goodIP = userInput(userIP)
    if goodIP == ValueError:
        error = "Invalid entry, please try again!"
        return render_template("index.html", error=error)
    
    # valid ip is processed by ipDetail function to generate data for table builder
    ipList = ipDetail(userIP)
    return render_template("index.html", ipList=ipList)


##
# ALL FUNCTIONS UNDER HERE
##

# check to make sure user enters a valid ip address
def userInput(ip):
    """ Uses ipaddress module to verify a valid IP is given
        Print an error message if it is invalid and prompt user to re-enter

        Keyword arguments:
        ip -- ip address or "Q" to quit, entered by user
    """
    print("This is the userInput function start")
    while True:
        try:
            if ipaddress.ip_interface(ip) != ValueError:
                print("\nNo value error\n\n")
                return ip
        except ValueError:
            print("\nValue error here\n\n")
            return ValueError
            

# prints out detailed information about user provided input
def ipDetail(ip):
    """ Uses ipaddress module to display information about the user entered IP and mask

        Keyword arguments:
        ip -- ip address entered by user
    """
    ipDict = {}         # used to create the dictionary objects that are placed in the tuples in the list
    ipList = []         # the list of tuples containing the ip info to return
    ipInt = ipaddress.ip_interface(ip)    # object to extract 
    ipNet = ipInt.network    # object to extract subnet host is on and to obtain the netmask
    ipNetwork = ipaddress.ip_network(ip, strict=False)    # object to extract 

# print the given ip address and its binary equivalent
    ipTmp = ip.split('/')
    ipOnly = ipTmp[0]
    ipBinary = '.' .join(format(int(i), "08b") for i in ipOnly.split("."))
    ipDict[ipOnly] = ipBinary
    ipList.append(("Address:", ipOnly, ipBinary))

# print out the netmask and its binary equivalent
    netmaskBinary = '.' .join(format(int(i), "08b") for i in (str(ipNet.netmask)).split("."))
    netMask = str(ipNet.netmask)
    ipDict[netMask] = netmaskBinary
    ipList.append(("Netmask:", netMask, netmaskBinary))

# print out the wildcard mask and its binary equivalent
    hostmaskBinary = '.' .join(format(int(i), "08b") for i in (str(ipNet.hostmask)).split("."))
    hostMaskOnly = str(ipNet.hostmask)
    ipDict[hostMaskOnly] = hostmaskBinary
    ipList.append(("Wildcard:", hostMaskOnly, hostmaskBinary))

# print out the network and its binary equivalent
    ipnetTmp = str(ipNet).split("/")
    ipnetOnly = str(ipNet)
    subnetBinary = '.' .join(format(int(i), "08b") for i in (str(ipnetTmp[0])).split("."))
    ipDict[ipnetOnly] = subnetBinary
    ipList.append(("Network:", ipnetOnly, subnetBinary))

# print out the broadcast and its binary equivalent
    if str(ipInt.netmask) != "255.255.255.255":     # this helps the handling of host only addresses, and avoids indexing issues
        bcastBinary = '.' .join(format(int(i), "08b") for i in (str(ipInt.network.broadcast_address)).split("."))
        bcastAddress = str(ipInt.network.broadcast_address)
        ipDict[bcastAddress] = bcastBinary
        ipList.append(("Broadcast:", bcastAddress, bcastBinary))

# print out the first host and its binary equivalent
    if str(ipInt.netmask) != "255.255.255.255":     # this helps the handling of host only addresses, and avoids indexing issues
        firstTmp = ipNetwork[1]
        firstHost = str(firstTmp)
        firstHostBinary = '.' .join(format(int(i), "08b") for i in str(firstTmp).split("."))
        ipDict[firstHost] = firstHostBinary
        ipList.append(("FirstHost:", firstHost, firstHostBinary))

# print out the last host and its binary equivalent
    if str(ipInt.netmask) != "255.255.255.255":     # this helps the handling of host only addresses, and avoids indexing issues
        lastTmp = ipNetwork[-2]
        lastHost = str(lastTmp)
        lastHostBinary = '.' .join(format(int(i), "08b") for i in str(lastTmp).split("."))
        ipDict[lastHost] = lastHostBinary
        ipList.append(("LastHost:", lastHost, lastHostBinary))

# print out the number of hosts on the subnet
    if str(ipInt.netmask) != "255.255.255.255":     # this helps the handling of host only addresses, and avoids indexing issues
        availTmp = int(lastTmp) - int(firstTmp)
        availHosts = str(availTmp)
        ipDict["AvailHosts"] = availHosts
        ipList.append(("AvailHosts", availHosts))

# return the list of tuples
    return ipList

##
# END
##