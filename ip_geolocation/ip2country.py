import csv
from netaddr import *

with open("GeoIPCountryWhois.csv") as csv_file:
    read_csv = csv.reader(csv_file, delimiter=",")
    what_ip = input("What IP should be looked up? ")

    for row in read_csv:
        ip_low = IPAddress(row[0])
        ip_high = IPAddress(row[1])
        country = row[4]

        if IPAddress(what_ip) >= ip_low and IPAddress(what_ip) <= ip_high:
            print(country)
