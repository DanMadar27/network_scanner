import sys
import json
from pysnmp.hlapi import *

def snmp_ip_addresses():  # ip addresses of computers that using snmp
    tree_ip = []
    for i in range(1, len(sys.argv)):
        tree_ip.append(sys.argv[i])
    return tree_ip


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


def Write_Json(lst):  # write the data about my computer and the router to a json file
    with open(
        r"D:\MyFolder\Json and Pickle files\computers_upTime_updates.json", "w"
    ) as handle:
        json.dump(lst, handle)


lst = []
snmp_ip = snmp_ip_addresses()
for ip in snmp_ip:
    upTime = getSysUpTime(ip)
    d = {"ip": ip, "upTime": upTime}
    lst.append(d)
Write_Json(lst)
