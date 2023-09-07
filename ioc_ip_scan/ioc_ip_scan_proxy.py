#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:19:05 2023
https://nmap.org/book/man-bypass-firewalls-ids.html
Warning: this feature is still under development and has limitations.
It is implemented within the nsock library and thus has no effect on the ping,
port scanning and OS discovery phases of a scan. Only NSE and version scan
benefit from this option so far—other features may disclose your true address.
SSL connections are not yet supported, nor is proxy-side DNS resolution
(hostnames are always resolved by Nmap).
@author: fan.z
https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4.txt

┌──(kali㉿kali)-[~/nmap]
└─$ pip install python-nmap

"""

import nmap

INPUT_FILE = 'ipiocs.txt'
PROXY_LIST = 'proxy-list.txt'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    ips = f.readlines()

with open(PROXY_LIST, 'r', encoding='utf-8') as p:
    PROXIES = ','.join(['socks4://'+line.strip() for line in p.readlines()])

nm = nmap.PortScanner()

for ip in ips:
    nm.scan(hosts=ip, arguments=PROXIES)
    csv_data = nm.csv().replace(';', ',')
    print(csv_data)
    with open('scan_'+ip.rstrip() + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(csv_data)

print('\nWell done... ')
