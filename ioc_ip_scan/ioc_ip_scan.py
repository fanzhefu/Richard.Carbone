#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:19:05 2023

@author: fan.z
"""

import nmap

INPUT_FILE = 'ipiocs.txt'

with open(INPUT_FILE, 'r') as f:
    ips = f.readlines()

nm = nmap.PortScanner()

for ip in ips:
    nm.scan(ip)
    csv_data = nm.csv().replace(';', ',')
    print(csv_data)
    with open('scan_'+ip.rstrip() + '.csv', 'w', newline='') as csvfile:
        csvfile.write(csv_data)

print('\nWell done... ')
