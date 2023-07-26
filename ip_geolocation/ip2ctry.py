# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 09:19:24 2023

@author: fanzhefu
"""

import csv
import socket
import struct

from bisect import bisect_left


def ip2long(ip_addr):
    """
    Convert an IP string to long 
    """
    packed_ip = socket.inet_aton(ip_addr)
    return struct.unpack("!L", packed_ip)[0]


class GeoIPCountry():
    def __init__(self, geoips_file):
        """
        Load IP range location map from CSV file filling in any empty ranges as
        we go. Assumes that the data in geoips_file is sorted by IP address.
        """
        rows = csv.reader(geoips_file)
        self.geoips = []
        last_hi = 0
        for row in rows:
            if int(row[2]) != last_hi+1:
                self.geoips.append((last_hi+1, int(row[2])-1, None, None))
            self.geoips.append((int(row[2]), int(row[3]), row[4], row[5]))
            last_hi = int(row[3])
        if last_hi < ip2long('255.255.255.255'):
            self.geoips.append(
                (last_hi+1, ip2long('255.255.255.255'), None, None))
        self.keys = [geoip[1] for geoip in self.geoips]
#        assert sorted(self.keys) == self.keys

    def lookup_country(self, ip_address):
        """
        Return tuple of country code and country name for an IP address.
        """
        return self.geoips[bisect_left(self.keys, ip2long(ip_address))][-2:]


if __name__ == '__main__':
    with open('GeoIPCountryWhois.csv',encoding='utf-8') as csv_file:
        geoip = GeoIPCountry(csv_file)

    for ip in ('0.1.2.3', '1.2.3.4', '192.168.1.1', '203.123.4.23',
                       '123.132.123.123', '223.255.255.255', '255.255.255.255'):
        country = geoip.lookup_country(ip)
        if country[0] is not None:
            print("{:<15} -> {} ({})".format(ip,
                  country[1], country[0]))
        else:
            print("{:<15} -> unknown".format(ip))
