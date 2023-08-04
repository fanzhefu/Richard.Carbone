# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 16:24:53 2023

@author: fan.z
"""
import os
import json
import requests

MY_USER_NAME = 'richard.carbone@forces.gc.ca'
MY_API_KEY = '9551eebddd72e8bf7c33caa9ff4e233fb4357c29'
TYPE = ['ip', 'hash', 'url', 'domain']
FEED_ID = {'CCCS': 6727, 'PolySwarm': 5359, 'Cybersixgill': 3549, 'NixSpam': 2334, 
           'URLHaus': 2656, 'Open_Phish_Feed': 136, 'Blocklist_Apache_Attacks': 104, 
           'cinsscore_ci_badguys_OSINT': 2518, 'TOR_Exit_Nodes': 122, 
           'PhishStats_PhishScore': 5068, 'Snort_IP_BlockList': 263, 
           'CI_Army': 18, 'Botscout_BOT_IPs': 141, 'PhishTank': 477, 
           'Blocklist_Bots': 103, 'blocklist_greensnow_OSINT': 2515, 
           'Bot_Scout_IP': 77, 'VoIP_Blacklist': 280, 
           'VoIP_Blacklist_by_ScopServ': 156, 'Haleys_Brute_Force_IPs': 142,
           'Spamhaus_Drop_List': 259, 'IAT_Blocklist': 2195, 
           'Nuug_Pop3_Groper_Web': 2196, 'Spamhaus_Extended_Drop_List': 260, 
           'Emerging_Threats_Compromised_IPS': 2056, 'ISC_SANS_Source_IPs': 193, 
           'Anomali_Twitter': 7139, 'Project_Honeypot': 20, 'SANS_top_IPs': 389, 
           'Feodotracker_CnC_Hosts': 497, 'Talos_Intelligence_IP_Blacklist': 2008, 
           'VX_Vault_Malware': 167, 'vxvault_URLs': 322, 'fedotracker': 431, 
           'SSL_Malware_Blacklist': 258, 'abuse_ch_SSL_Blacklist': 2664, 
           'Sans_Internet_Storm_Center_miner': 2009}

def parseIndicators(streamArray, fname_json):
    for stream in streamArray:
        indent_stream = json.dumps(stream, indent=2)
        # print (indent_stream)
        with open(fname_json, "a", encoding="utf-8") as f:
            f.write(f"{indent_stream}" + '\n')

for my_type in TYPE:
    if not os.path.exists(my_type):
        os.makedirs(my_type)
    print(my_type+':')

    for key, value in FEED_ID.items():
        print('\t', key, value)
        my_feed_id = str(value)
        url = 'https://api.threatstream.com/api/v2/intelligence/?username=' + MY_USER_NAME + '&api_key=' + MY_API_KEY + \
            '&status=active&FEED_ID=' + my_feed_id + '&type=' + my_type + \
            '&created_ts__gte=2023-06-07T04:00:00.000Z&confidence__gte=80'

        response = requests.get(url)
        fname_json = my_type + '/' + key + '.json'
        print('\t', 'writing file: ' + fname_json + '')
        parseIndicators(response.json()['objects'], fname_json)

print('\n\n', 'Check output in directories: ip, hash, url, domain')