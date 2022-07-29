#!/usr/bin/python3

# Matt Perry 7-28-2022
# Finds available public IP subnets between /24 and /27 in provided route lists

import paramiko
import re
import csv
import tik_ssh
import creds
import threading
import concurrent.futures
from pathlib import Path
from ipaddress import ip_address,ip_interface,ip_network

# Global Variables

thread_local = threading.local()

# List to hold router names and Number of private leases
lease_list = []

# path to routers.csv and output.csv
current_dir = Path.cwd()
router_file = current_dir / 'routers.csv'
output_file = current_dir / 'output.csv'

# private dhcp range
private_range = '172.16.0.0/12'

def load_routers(path):
    #list to hold router names and IP
    routers = []
    
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            routers.append([row[0], row[1]])
    
    return routers
    
def insert_leases(router):    
    router_name = router[0]
    ip = router[1]
    
    ssh = tik_ssh.connect(str(ip), creds.username, creds.password)
    
    if ssh != None:
        command = f"/ip dhcp-server lease print count-only where status=bound and address in {private_range}"
    
    output = tik_ssh.command(ssh, command)
    
    lease_list.append([router_name, ip, output[0]])
    

def poplulate_leases(routers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        executor.map(insert_leases,routers)

def output_csv(output_file):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        
        for line in lease_list:
            if int(line[2]) > 0:
                writer.writerow(line)

def main():
    routers = load_routers(router_file)
        
    poplulate_leases(routers)
    
    output_csv(output_file)

if __name__ == "__main__":
    main()
