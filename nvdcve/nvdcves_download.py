# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 09:38:27 2023

download all cve json zip files

@author: fanzhefu
"""
import os
import re
import requests

OUTPUT_DIR = "zip"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
r = requests.get('https://nvd.nist.gov/vuln/data-feeds#JSON_FEED')
for filename in re.findall("nvdcve-1.1-[0-9]*\.json\.zip", r.text):
    print(filename)
    url = "https://nvd.nist.gov/feeds/json/cve/1.1/" + filename
    print(url)
    r_file = requests.get(url, stream=True)
    with open(OUTPUT_DIR +'/'+ filename, 'wb') as f:
        for chunk in r_file:
            f.write(chunk)

print("\nWell done !!!")
