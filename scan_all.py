import subprocess
import multiprocessing
import socket
import json
import time
import cmdInteracting
import pickle
from pysnmp.hlapi import *
import sys
import threading

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

def Write_Json(manager_list):  # write the list of computers to json file
    new_lst = []
    for m in manager_list:
        new_lst.append(m)
    with open(r"D:\MyFolder\Json and Pickle files\new_computers.json", "w") as handle:
        json.dump(new_lst, handle)

def Write_Pickle(x):  # write the valid ip addresses to *.txt file
    with open(
        r"D:\MyFolder\Json and Pickle files\valid_ip_addresses.txt", "w"
    ) as handle:
        pickle.dump(x, handle)

def Load_Pickle():  # return the valid ip addresses from *.txt file
    with open(
        r"D:\MyFolder\Json and Pickle files\valid_ip_addresses.txt", "r"
    ) as handle:
        x = pickle.load(handle)
    return x


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

def getSysName(host):  # return the computer's name
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
        return ""

def getSysDescription(host):  # return description about the computer's operating system
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
        return ""

def getSysContact(host):  # return the computer's contact name
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
        return ""

def getSysLocation(host):  # return the copmuter's location
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
        return ""

def divideList(lst):  # divide list to equal parts
    if len(lst) >= 5:  # len of list is greater or equal to 5
        n = len(lst) / 5
        new_list = []
        for i in range(0, len(lst), n):
            new_list.append(lst[i : i + n])
        return new_list
    elif len(lst) > 0:  # len of list is between 0 to 5
        return lst
    return []

def pingRange(ip_list, lst, valid_ip, process_lock):  # pings the list of ip addresses
    thread_lock = threading.Lock()
    divided_ip_list = divideList(ip_list)
    all_threads = []
    if len(divided_ip_list) > 0:
        for new_ip_list in divided_ip_list:
            t = threading.Thread(
                target=pingRange2,
                args=(
                    new_ip_list,
                    lst,
                    valid_ip,
                    process_lock,
                    thread_lock,
                ),
            )
            t.start()
            all_threads.append(t)
        for t in all_threads:
            t.join()


def pingRange2(
    ip_list, lst, valid_ip, process_lock, thread_lock
):  # pings the list of ip addresses
    for ip in ip_list:
        if not (ip in valid_ip) and (ip != cmdInteracting.myIP()):
            valid = ping(ip, lst, process_lock, thread_lock)
            if valid:
                thread_lock.acquire()
                process_lock.acquire()
                valid_ip.append(ip)
                Write_Pickle(valid_ip)  # write the valid ip address to *.txt file
                print "%s is valid"%ip
                thread_lock.release()
                process_lock.release()


def ping(ip, lst, process_lock, thread_lock):  # ping ip address
    p = subprocess.Popen(["ping", "-n", "1", "-w", "1000", ip], stdout=subprocess.PIPE)
    p.wait()
    if not p.poll():  # if there was reply
        output = subprocess.Popen(
            ["arp", "-a", ip], stdout=subprocess.PIPE
        ).communicate()[0]
        if (
            output.lower() != "no arp entries found.\r\n"
        ):  # if could get mac address of the computer
            mac = output.split()[-2]
            m = Machine(ip, mac, hostname(ip))
            d = m.dict()
            thread_lock.acquire()
            process_lock.acquire()  # prevent processes to access with the same time to the json file
            lst.append(d)
            Write_Json(lst)  # write the new machine to json file
            thread_lock.release()
            process_lock.release()
            return True
    return False


def hostname(ip):  # return hostname of the computer by its ip address
    name = socket.getfqdn(ip)
    if name == ip:
        return "Unknown hostname"
    return name


def startScan():  # start scanning the local network
    manager = multiprocessing.Manager()  # manager that handle the processes
    lst = manager.list()  # list of machines
    all_process = []  # list of processes
    all_ip = (
        cmdInteracting.getAll_IP()
    )  # list that every element is list of ip addresses
    valid_ip = manager.list()
    lock = multiprocessing.Lock()
    try:
        valid_ip_file = (
            Load_Pickle()
        )  # try loading valid_ip_addresses in case of that we scanned the local network before
        for ip in valid_ip_file:
            valid_ip.append(ip)
    except:
        pass
    for x in all_ip:  # creating process to each list of ip addresses
        p = multiprocessing.Process(
            target=pingRange,
            args=(
                x,
                lst,
                valid_ip,
                lock,
            ),
        )
        p.start()
        all_process.append(p)

    for p in all_process:
        p.join()

    valid_ip_new = []
    for ip in valid_ip:
        valid_ip_new.append(ip)
    Write_Pickle(valid_ip_new)  # writes the valid ip addresses in *.txt file
    # new_lst=[]
    # for m in lst:
    #    new_lst.append(m)
    # return new_lst


def PrintTimePassed(start):  # print the time passed since the "start" argument
    timePassed = int(time.time() - start)
    if timePassed >= 60:
        minutes = timePassed / 60
        seconds = timePassed % 60
        if seconds!=0:
            print "took %s minutes and %s seconds"%(minutes,seconds)
        else:
            print "took %s minutes"%(minutes)
    else:
        print "took %s seconds"%(timePassed)

def Main():  # main
    start = time.time()
    startScan()  # start scanning
    PrintTimePassed(start)  # print how much time passed


if __name__=="__main__":
    Main()
    while True:
        s = raw_input(r"start scan?(y/n)"+"\n") #asks the user to start scan
        if s == "n":
            sys.exit()
        elif s == "y":
            Main()
        else:
            print "enter valid keyword"
