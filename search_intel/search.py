# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 09:15:49 2023

@author: fan.z

search database table by value, source, threat-actor and malware
eg:
$search -t ipv4 -a apt0 -m panda

"""

import argparse
import sqlite3
# import os

DB_FILE = "TESTDATA.db"

parser = argparse.ArgumentParser(
    description='Search the database by type(fqdn, ipv4, url, md5), \
        value, source, actor, or malware .')
parser.add_argument('-t', metavar='type',  type=str, dest='table',
                    required=True, help='type(fqdn, ipv4, url, and md5)')
parser.add_argument('-v', metavar='value', type=str, nargs='?', dest='value',
                    help='the value of type(fqdn, ipv4, url, and md5)')
parser.add_argument('-s', metavar='source', type=str, nargs='?', dest='source',
                    help='the name of source')
parser.add_argument('-a', metavar='actor', type=str, nargs='?', dest='actor',
                    help='the name of actor')
parser.add_argument('-m', metavar='malware', type=str, nargs='?', dest='malware',
                    help='the name of malware')

args = parser.parse_args()
table = args.table
value = args.value if args.value else '_'
source = args.source if args.source else '_'
actor = args.actor if args.actor else '_'
malware = args.malware if args.malware else '_'
#print(table, value, source, actor, malware)


with sqlite3.connect(DB_FILE) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT * FROM '{table}' WHERE value LIKE '%{value}%' AND \
            sources LIKE '%{source}%' AND threat_actors LIKE '%{actor}%' AND \
                malwares LIKE '%{malware}%'  """)
    #print(f"""SELECT * FROM {table} WHERE threat_actors LIKE %{actor}% AND malwares LIKE %{malware}%  """)
    for row in cursor:
        print(list(row))
