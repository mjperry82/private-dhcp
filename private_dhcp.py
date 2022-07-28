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

def load_routers(path):
    
def insert_leases(routers):
    

def poplulate_leases(routers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(insert_leases,routers)

def main():
    routers = load_routers(path)
    
    populate_leases(routers)

if __name__ == "__main__":
    main()
