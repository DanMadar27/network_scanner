import json
import subprocess
import cmdInteracting
import pickle
import time
import sys

def ping(ip): #return True or False if the host is up or down
    p=subprocess.Popen(["ping","-n","1","-w","1000",ip],stdout=subprocess.PIPE)
    p.wait()
    if p.poll(): #no reply
        return False
    return True

def Write_Json(x): #writing json file
    with open(r"D:\MyFolder\Json and Pickle files\shutdown_computers.json","w") as handle:
        json.dump(x,handle)
    
def tree_ip_addresses(): #get ip addresses from the tree
    tree_ip=[]
    for i in range(1,len(sys.argv)):
        tree_ip.append(sys.argv[i])
    return tree_ip


lst=[] # [{"ip": "1.1.1.1" , valid:True} , {"ip": "2.2.2.2" , valid:False}]
try:
    valid_ip=tree_ip_addresses()
    print(valid_ip)
    for ip in valid_ip:
        dict={"ip":ip}
        if ping(ip): #if there was reply
            dict["valid"]=True
        else:
            dict["valid"]=False
        lst.append(dict)        
    Write_Json(lst) #writing the list to json file
except:
    pass
   