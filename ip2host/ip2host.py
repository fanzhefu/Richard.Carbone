# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 16:54:32 2023

@author: fan.z
"""

#!/usr/bin/python
import socket
ips = open('ip.txt').readlines()

for ip in ips:
    try:
        host = socket.gethostbyaddr(ip.rstrip())
        print(host[-1][0]+'\t'+host[0])
    except Exception as e:
        # print(ip.rstrip()+'\t'+'host-not-found')
        continue
