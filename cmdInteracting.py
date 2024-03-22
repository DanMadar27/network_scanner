import subprocess
import sys

def get_ip_mac_routerIP_subnetMask():
    # get output of cmd commdand: "ipconfig /all"
    output = subprocess.Popen(
        ["ipconfig", "/all"], stdout=subprocess.PIPE
    ).communicate()[0]
    lines = output.split("\n")  # seperate each line of the output
    for i in range(len(lines)):
        if (
            "Wireless Network Connection" in lines[i]
            or "Local Area Connection" in lines[i]
        ):
            # the required info is in these lines
            x = lines[i + 2 : i + 19]
            break

    ip = ""
    mac = ""
    router_ip = ""
    mask = ""
    for line in x:
        if "IPv4 Address" in line:  # if line of my ip address
            start = line.find(":") + 2
            ip = line[start:-13]

        elif "Physical Address" in line:  # if line of my mac address
            start = line.find(":") + 2
            mac = line[start:-1]

        elif "Default Gateway" in line:  # if line of my default gateway ip
            start = line.find(":") + 2
            router_ip = line[start:-1]

        elif "Subnet Mask" in line:  # if line of my subnetMask
            start = line.find(":") + 2  #
            mask = line[start:-1]

    flag = True
    if ip == "":  # if couldn't find my ip
        print "Something wrong when getting my ip in cmdInteracting.py file"
        flag = False
    if mac == "":  # if couldn't find my mac address
        print "Something wrong when getting my mac address in cmdInteracting.py file"
        flag = False
    if router_ip == "":  # if couldn't find my router_ip
        print "Something wrong when getting router ip in cmdInteracting.py file"
        flag = False
    if mask == "":  # if couldn't find my subnet mask
        print "Something wrong when getting mask in cmdInteracting.py file"
        flag = False

    if flag:
        return (ip, mac, router_ip, mask)
    else:
        sys.exit()


def binaryToDecimal(num):  # convert binary number to decimal
    return int(num, 2)


def decimalToBinary(num):  # convert decimal number to 8 bits- binary number
    return "{0:08b}".format(num)


def add(num):  # add 1 to a binary number
    s = num[:-1]
    if num[-1] == "0":
        s += "1"
    else:
        s += "2"
    s = check_if_need_to_reset(s)
    return s


def check_if_need_to_reset(
    num,
):  # check if there isn't number different then 0 or 1 in the binary number
    lst = list(num)
    for i in range(len(lst) - 1, 0, -1):
        if lst[i] != "0" and lst[i] != "1":
            lst[i] = "0"
            if lst[i - 1] == "0":
                lst[i - 1] = "1"
            else:
                lst[i - 1] = "2"
    return "".join(lst)


def bitsToBytes(bits):  # convert bits to byte
    lst = []
    s = ""
    count = 0
    for b in bits:
        s += b
        count += 1
        if count == 8:
            lst.append(s)
            s = ""
            count = 0
    return lst


def listToIP(lst):  # convert list (lst=["10","0","0","5"]) of string to ip
    s = ""
    for i in range(len(lst) - 1):
        s += str(lst[i]) + "."
    s += str(lst[-1])
    return s


def bitsToIP(bits):  # convert bits to ip
    lst = bitsToBytes(bits)
    for i in range(len(lst)):
        lst[i] = binaryToDecimal(lst[i])
    return listToIP(lst)


def ipToBits(ip):  # convert ip to bits
    s = ""
    lst = ip.split(".")
    for n in lst:
        s += decimalToBinary(int(n))
    return s


def startEnd(mask):  ##split between ones and zeroes of mask
    mask = ipToBits(mask)
    start = ""
    end = ""

    for b in mask:
        if b == "1":
            start += b
        else:
            end += b
    return (start, end)


def all_numbers(num):  # all combinations of possible bits of the subnet mask
    flag = True
    lst = []
    while flag:
        lst.append(num)
        if not "0" in num:
            flag = False
        num = add(num)
    return lst


def getAll_IP():
    ip = myIP()
    mask = subnetMask()
    start, end = startEnd(mask)
    ip = ipToBits(ip)  # my ip to bits, get start of all ip in bits
    myStart = ""
    for i in range(len(start)):
        myStart += ip[i]
    lst = all_numbers(end)
    for i in range(len(lst)):
        lst[i] = bitsToIP(myStart + lst[i])
    for x in lst:
        if x[-1] == "0" or x[-3:] == "255":  # check if ip is valid ip address
            lst.remove(x)
    n = len(lst) / 5
    new_list = []
    for i in range(0, len(lst), n):
        new_list.append(lst[i : i + n])
    return new_list


def routerMacAddress2():  # get the router's mac address
    ip = router_ip
    mac = ""
    # pinging the router and then get his mac address
    subprocess.Popen(["ping", "-n", "1", "-w", "1000", ip], stdout=subprocess.PIPE)
    output = subprocess.Popen(["arp", "-a", ip], stdout=subprocess.PIPE).communicate()[
        0
    ]
    if output.lower() != "no arp entries found.\r\n":
        mac = output.split()[-2]
    if mac != "":  # if got the router's mac
        return mac
    else:
        print "Something wrong when trying to get router ip address"

my_ip, mac, router_ip, mask = get_ip_mac_routerIP_subnetMask()
router_mac = routerMacAddress2()


def myIP():  # return my ip address
    return my_ip


def myMacAddress():  # return my mac address
    return mac


def routerIP():  # return router's ip address
    return router_ip


def routerMacAddress():  # return router's mac address
    return router_mac


def subnetMask():  # return subnet mask
    return mask
