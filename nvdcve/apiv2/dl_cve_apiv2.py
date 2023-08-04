# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 17:05:41 2023

@author: fan.z
"""

import datetime
import json
import requests

YEAR = '2023'

# The maximum allowable range when using any date range parameters is 120 consecutive days.
BASE_URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
pub_start_date = [YEAR+'-'+'01'+'-01', YEAR+'-'+'04' +
                  '-01', YEAR+'-'+'07'+'-01', YEAR+'-'+'10'+'-01']
pub_end_date = [YEAR+'-'+'04'+'-01', YEAR+'-'+'07' +
                '-01', YEAR+'-'+'10'+'-01', YEAR+'-'+'01'+'-01']

print('\nDownloading ... ...')
for i in range(4):
    if datetime.datetime.now() > datetime.datetime(*map(int, pub_start_date[i].split('-'))):
        #         print(i)
        params = {"pubStartDate": pub_start_date[i]+'T00:00:00.000',
                  "pubEndDate": pub_end_date[i]+'T00:00:00.000'}
        response = requests.get(BASE_URL, params).json()
        vulns = response['vulnerabilities']

        for vuln in vulns:
            print(vuln['cve']['id'],end=', ')
            with open(YEAR+'.json', 'a', encoding='utf-8') as f:
                json.dump(vuln, f, ensure_ascii=False, indent=4)

print('\n\nDone, check the file "'+YEAR+'.json" for all the CVEs')