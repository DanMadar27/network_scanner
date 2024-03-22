import cmdInteracting
import socket
import json
from pysnmp.hlapi import *

class Machine:
    def __init__(self, ip, mac, hostname):  #
        self.ip = ip
        self.mac = mac
        self.hostname = hostname
        self.myComputer = ip == cmdInteracting.myIP()
        self.router = ip == cmdInteracting.routerIP()
        if self.router and self.hostname == "Unknown hostname":
            self.hostname = "Router"
        self.isUsingSNMP = isSNMP(self.ip)
        if self.isUsingSNMP:
            self.sysUptime = getSysUpTime(self.ip)
            self.sysName = getSysName(self.ip)
            self.sysDescription = getSysDescription(self.ip)
            self.sysContact = getSysContact(self.ip)
            self.sysLocation = getSysLocation(self.ip)

    def dict(self):  # convert the machine do dictionary
        d = {}
        d["ip"] = self.ip
        d["mac"] = self.mac
        d["hostname"] = self.hostname
        d["myComputer"] = self.myComputer
        d["router"] = self.router
        d["isUsingSNMP"] = self.isUsingSNMP
        if self.isUsingSNMP:
            d["sysUptime"] = self.sysUptime
            d["sysName"] = self.sysName
            d["sysDescription"] = self.sysDescription
            d["sysContact"] = self.sysContact
            d["sysLocation"] = self.sysLocation
        return d

    def __str__(self):
        return str(self.dict())

def hostname(ip):  # return hostname of the computer by its ip address
    name = socket.getfqdn(ip)
    if name == ip:
        return "Unknown hostname"
    return name

def get_router():  # return instance of machine that represent the router
    ip = cmdInteracting.routerIP()
    mac = cmdInteracting.routerMacAddress()
    hostname = "Router"
    m = Machine(ip, mac, hostname)
    return m

def get_myComputer():  # return instance of machine that represent my computer
    ip = cmdInteracting.myIP()
    mac = cmdInteracting.myMacAddress()
    hostname = socket.gethostname()
    m = Machine(ip, mac, hostname)
    return m


def Write_Json(lst):  # write the data about my computer and the router to a json file
    with open(
        r"D:\MyFolder\Json and Pickle files\myComputer_router.json", "w"
    ) as handle:
        json.dump(lst, handle)

def isSNMP(host):  # return True or False if the computer is using SNMP services
    g = getCmd(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysUpTime", 0)),
    )
    try:
        next(g)[3][0][1]
        return True
    except:
        return False

def getSysUpTime(ip):
    g = getCmd(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysUpTime", 0)),
    )
    try:
        x = int((next(g)[3][0][1])) / 6000
        if x > 60:  # time is greater than 60 minutes
            return "%s hours and %s minutes" % (x / 60, x % 60)
        return "%s minutes" % (x % 60)
    except IndexError:
        return ""

def getSysName(host):  # returns the computer's name
    g = getCmd(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
    )
    try:
        x = next(g)[3][0][1]
        return str(x)
    except IndexError:
        print("list index is out of range in getSysName function")

def getSysDescription(
    host,
):  # returns description about the computer's operating system
    g = getCmd(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )
    try:
        x = next(g)[3][0][1]
        return str(x)
    except IndexError:
        print("list index is out of range in getSysDescription function")

def getSysContact(host):  # returns the computer's contact name
    g = getCmd(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysContact", 0)),
    )
    try:
        x = next(g)[3][0][1]
        return str(x)
    except IndexError:
        print("list index is out of range in getSysContact function")

def getSysLocation(host):  # the computer's location
    g = getCmd(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysLocation", 0)),
    )

    try:
        x = next(g)[3][0][1]
        return str(x)
    except IndexError:
        print("list index is out of range in getSysLocation function")

lst = []
# getting my computer and the router
myComputer = get_myComputer().dict()  # g
router = get_router().dict()
lst.append(myComputer)
lst.append(router)
Write_Json(lst)  # write my copmuter and the router to json file
