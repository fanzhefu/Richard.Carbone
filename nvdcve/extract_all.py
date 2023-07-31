# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:24:08 2023

Extract all data from nvd cves

@author: fanzhefu
"""
import os
import sys
import json
import zipfile

INPUT_DIR = "zip"
OUTPUT_DIR = "txt"

if not os.path.exists(INPUT_DIR):
    print('\nPlease download nvd cves first...')
    sys.exit(0)
    
if os.path.exists(OUTPUT_DIR):
    print('\nRename directory "'+OUTPUT_DIR+'", and try again. ')
    sys.exit(0)
else:
    os.makedirs(OUTPUT_DIR)
print('\nStarting processing ...')        
for input_file in os.listdir(os.fsencode(INPUT_DIR) ):
    INPUT_FILE = INPUT_DIR +'/'+ input_file.decode("utf-8")
    OUTPUT_FILE = OUTPUT_DIR +'/'+ input_file.decode("utf-8").strip('json.zip')+'.txt'
    #print(INPUT_FILE, OUTPUT_FILE)
    
    with zipfile.ZipFile(INPUT_FILE, "r") as z:
        for filename in z.namelist():
            #       print(filename)
            with z.open(filename) as f:
                json_raw = f.read().decode('utf-8')
                json_data = json.loads(json_raw)
                
    print(OUTPUT_FILE)
    for entry in json_data['CVE_Items']:
    
        identity = entry['cve']['CVE_data_meta']['ID']
        assigner = entry['cve']['CVE_data_meta']['ASSIGNER']
        try:
            problemtype = entry['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']
        except IndexError:
            problemtype = ''
    
        urls = ', '.join([item['url']
                          for item in entry['cve']['references']['reference_data']])
        description = entry['cve']['description']['description_data'][0]['value']
    
        try:
            configurations = ', '.join(
                [item['cpe23Uri'] for item in entry['configurations']['nodes'][0]['cpe_match']])
        except IndexError:
            configurations = ''
    
        try:
            impact = entry['impact']['baseMetricV3']['cvssV3']
            impacts = impact['attackVector']+' | '+impact['attackComplexity'] + \
                ' | '+impact['privilegesRequired']+' | '+impact['userInteraction'] + \
                ' | '+impact['confidentialityImpact']+' | '+impact['integrityImpact'] + \
                ' | '+impact['availabilityImpact']+' | '+impact['baseSeverity']
        except KeyError:
            impacts = ''
            
        
        #print('.', end='')
        # print(identity+' | '+assigner+' | '+problemtype+' | '+urls +
        #      ' | '+description+' | '+configurations+' | '+impacts)
    
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as output_file:
            output_file.write(identity+' | '+assigner+' | '+problemtype+' | '+urls +
                              ' | '+description+' | '+configurations+' | '+impacts+'\n')
print("\nWell done !!!")
