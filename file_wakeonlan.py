from wakeonlan import wol
import sys


def turnOn(mac):  # turn on the computer with the given mac address
    wol.send_magic_packet(mac)


mac = sys.argv[1]  # get mac address from the arguments given
mac = mac.replace("-", ".")  # mac="ff-ff-ff-ff-ff-ff" need to be "ff.ff.ff.ff.ff.ff"
mac = mac.lower()  # change capital letters to small letters
turnOn(mac)  # turning on the copmuter
