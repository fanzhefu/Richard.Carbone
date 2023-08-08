# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 17:05:41 2023

download the nvd cves of nist.gov by year

@author: fan.z
"""
import datetime as dt
import json
import requests

# The year of all the CVEs to be downloaded.
YEAR = 2023

BASE_URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0?'
API_KEY = '168227f8-1383-4874-8275-470c4a96855e'


def dl_cves(year: str):
    '''
    Parameters
    ----------
    year : str
        The year of the CVEs to be downloaded.

    Returns
    -------
    None.

    '''
    # The maximum allowable range when using any date range parameters is 120 consecutive days.
    pub_start_date = [year+'-01-01T00:00:00.000', year+'-04-01T00:00:00.000',
                      year+'-07-01T00:00:00.000', year+'-10-01T00:00:00.000']
    pub_end_date = [year+'-04-01T00:00:00.000', year+'-07-01T00:00:00.000',
                    year+'-10-01T00:00:00.000', year+'-12-31T23:59:59.999']

    print('\nDownloading ... ...')
    for i in range(4):
        if dt.datetime.now() > dt.datetime(*map(int, pub_start_date[i][:10].split('-'))):

            params = {"pubStartDate": pub_start_date[i],
                      "pubEndDate": pub_end_date[i]}
            headers = {'content-type': 'application/json', 'apiKey': API_KEY}

            response = requests.get(
                BASE_URL, params=params, headers=headers, timeout=30)

            print(response.status_code)
            #response.encoding = 'utf-8'
            vulns = response.json()['vulnerabilities']

            for vuln in vulns:
                print(vuln['cve']['id'], end=', ')
                with open(year+'.json', 'a', encoding='utf-8') as f_json:
                    json.dump(vuln, f_json, ensure_ascii=False, indent=4)

    print('\n\nDone, check the file "'+year+'.json" for all the CVEs')


if __name__ == "__main__":
    dl_cves(str(YEAR))
