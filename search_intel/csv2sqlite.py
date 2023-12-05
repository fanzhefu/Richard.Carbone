# /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 15:34:31 2023

@author: fan.z
"""
'''
Converting TESTDATA.csv file into sqlite3 database
1. splite testdate file into four files: fqdn.csv, ipv4.csv, url.csv, md5.csv;
2. input fqdn.csv, ipv4.csv, url.csv, md5.csv into sqlit3 as four tables.
notes:
    hash column in md5 splited into sha1, sha256;
    didn't break down the columns sources, threat_actors and malwares
'''
#import pandas as pd
# importing csv module
import csv
import csv_to_sqlite

INPUT_FILE = 'TESTDATA.csv'

OUTPUT_FQDN = 'fqdn.csv'
OUTPUT_IPV4 = 'ipv4.csv'
OUTPUT_URL = 'url.csv'
OUTPUT_MD5 = 'md5.csv'
#OUTPUT_OTHER = 'other.csv'

fqdn_fields = ['score', 'value', 'last_seen_date', 'first_seen_date',
               'last_updated_date', 'sources', 'hash', 'threat_actors', 'malwares']
ipv4_fields = ['score', 'value', 'last_seen_date', 'first_seen_date',
               'last_updated_date', 'sources', 'hash', 'threat_actors', 'malwares']
url_fields = ['score', 'value', 'last_seen_date', 'first_seen_date',
              'last_updated_date', 'sources', 'hash', 'threat_actors', 'malwares']
md5_fields = ['score', 'value', 'last_seen_date', 'first_seen_date',
              'last_updated_date', 'sources', 'sha1', 'sha256', 'threat_actors', 'malwares']

# create four csv files and add the header
with open(OUTPUT_FQDN, 'w', newline='', encoding='utf-8') as csv_fqdn, \
        open(OUTPUT_IPV4, 'w', newline='', encoding='utf-8') as csv_ipv4, \
        open(OUTPUT_URL, 'w', newline='', encoding='utf-8') as csv_url, \
        open(OUTPUT_MD5, 'w', newline='', encoding='utf-8') as csv_md5:

    fqdn_writer = csv.writer(csv_fqdn)
    fqdn_writer.writerow(fqdn_fields)

    ipv4_writer = csv.writer(csv_ipv4)
    ipv4_writer.writerow(ipv4_fields)

    url_writer = csv.writer(csv_url)
    url_writer.writerow(url_fields)

    md5_writer = csv.writer(csv_md5)
    md5_writer.writerow(md5_fields)
    
    #process input csv file row by row
    with open(INPUT_FILE, 'r', encoding='utf-8') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        print('Processing csv file, please wait ... ')
        for row in csvreader:
            if row[1] == 'fqdn':
                del row[1]
                if row[7] != 'N/A':
                    row[7] = row[7].strip('{}')
                if row[8] != 'N/A':
                    row[8] = row[8].strip('{}')
                fqdn_writer.writerow(row)

            elif row[1] == 'ipv4':
                del row[1]
                if row[7] != 'N/A':
                    row[7] = row[7].strip('{}')
                if row[8] != 'N/A':
                    row[8] = row[8].strip('{}')
                ipv4_writer.writerow(row)

            elif row[1] == 'url':
                del row[1]
                if row[7] != 'N/A':
                    row[7] = row[7].strip('{}')
                if row[8] != 'N/A':
                    row[8] = row[8].strip('{}')
                url_writer.writerow(row)

            elif row[1] == 'md5':
                del row[1]
                if row[6] == 'N/A':
                    row.insert(6, 'N/A')
                else:
                    #md5 = row[6][10:42]
                    sha1 = row[6][56:96]
                    sha256 = row[6][-67:-3]
                    del row[6]
                    row.insert(6, sha256)
                    row.insert(6, sha1)
                if row[9] != 'N/A':
                    row[9] = row[9].strip('{}')
                if row[8] != 'N/A':
                    row[8] = row[8].strip('{}')
                md5_writer.writerow(row)

print("Import csv files into database:")
options = csv_to_sqlite.CsvOptions(typing_style="full", encoding="utf-8")
input_files = ["fqdn.csv", "ipv4.csv", "url.csv", "md5.csv"] # pass in a list of CSV files
csv_to_sqlite.write_csv(input_files, "output.sqlite", options)
print('Well done ...')
