# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 17:05:41 2023

@author: fan.z
"""

import datetime
import json
import requests

# Change the year for yourself
YEAR = '2023'

BASE_URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0?'
API_KEY = '168227f8-1383-4874-8275-470c4a96855e'

def dl_cves(YEAR):
    # The maximum allowable range when using any date range parameters is 120 consecutive days.
    pub_start_date = [YEAR+'-'+'01'+'-01', YEAR+'-'+'04' +
                      '-01', YEAR+'-'+'07'+'-01', YEAR+'-'+'10'+'-01']
    pub_end_date = [YEAR+'-'+'04'+'-01', YEAR+'-'+'07' +
                    '-01', YEAR+'-'+'10'+'-01', YEAR+'-'+'01'+'-01']
    
    print('\nDownloading ... ...')
    for i in range(4):
        if datetime.datetime.now() > datetime.datetime(*map(int, pub_start_date[i].split('-'))):
            #
            params = {"pubStartDate": pub_start_date[i]+'T00:00:00.000',
                      "pubEndDate": pub_end_date[i]+'T00:00:00.000'}
            headers = {'content-type': 'application/json', 'apiKey': API_KEY}
    
            response = requests.get(BASE_URL, params=params,
                                    headers=headers).json()
            vulns = response['vulnerabilities']
    
            for vuln in vulns:
                print(vuln['cve']['id'], end=', ')
                with open(YEAR+'.json', 'a', encoding='utf-8') as f:
                    json.dump(vuln, f, ensure_ascii=False, indent=4)
    
    print('\n\nDone, check the file "'+YEAR+'.json" for all the CVEs')

if __name__ == "__main__":
    dl_cves(YEAR)