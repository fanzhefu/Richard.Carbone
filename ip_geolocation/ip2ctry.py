# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 09:19:24 2023

@author: fan.z
"""

import csv
import socket
import struct

from bisect import bisect_left

def ip2long(ip):
    """
    Convert an IP string to long (see http://stackoverflow.com/a/9591005/21945)
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


class GeoIPCountry(object):
    def __init__(self, geoips_file):
        """
        Load IP range location map from CSV file filling in any empty ranges as
        we go. Assumes that the data in geoips_file is sorted by IP address.
        """
        r = csv.reader(geoips_file)
        self.geoips = []
        last_hi = 0
        for row in r:
            if int(row[2]) != last_hi+1:
                self.geoips.append((last_hi+1, int(row[2])-1, None, None))
            self.geoips.append((int(row[2]), int(row[3]), row[4], row[5]))
            last_hi = int(row[3])
        if last_hi < ip2long('255.255.255.255'):
            self.geoips.append((last_hi+1, ip2long('255.255.255.255'), None, None))
        self.keys = [geoip[1] for geoip in self.geoips]
#        assert sorted(self.keys) == self.keys

    def lookup_country(self, ip_address):
        """
        Return tuple of country code and country name for an IP address.
        """
        return self.geoips[bisect_left(self.keys, ip2long(ip_address))][-2:]


if __name__ == '__main__':
    with open('GeoIPCountryWhois.csv') as geoips_file:
        geoip = GeoIPCountry(geoips_file)

    for ip_address in ('0.1.2.3', '1.2.3.4', '192.168.1.1', '203.123.4.23',
                       '123.132.123.123', '223.255.255.255', '255.255.255.255'):
        country = geoip.lookup_country(ip_address)
        if country[0] is not None:
            print("{:<15} -> {} ({})".format(ip_address, country[1], country[0]))
        else:
            print("{:<15} -> unknown".format(ip_address))