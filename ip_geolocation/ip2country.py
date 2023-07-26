# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 11:32:15 2023

@author: fanzhefu
"""

import csv
#from ipaddress import *
import netaddr

with open("GeoIPCountryWhois.csv", encoding='utf-8') as csv_file:
    rows = csv.reader(csv_file, delimiter=",")
    what_ip = input("What IP should be looked up? ")

    for row in rows:
        ip_low = netaddr.IPAddress(row[0])
        ip_high = netaddr.IPAddress(row[1])
        country = row[4]

        if ip_low <= netaddr.IPAddress(what_ip) <= ip_high:
            print(country)
