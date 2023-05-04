# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:35:42 2023

@author: fan.z
"""
#/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import time
import random
import os

delay = 5 # 5 seconds btw connectiona 
years = [2020,2021,2022,'Current']  # read from the website

url_ic3 = "https://www.ic3.gov"
#read all user agents in
with open('user-agents.txt', 'r',  encoding='utf-8') as f:
    user_agents = f.readlines()

# the url of all the links
urls = []
for year in years:
    url_year= url_ic3 + '/Home/IndustryAlerts?pressReleasesYear=_' + str(year)
    random_user_agent  = random.choice(user_agents).rstrip()
    headers = {'User-Agent': random_user_agent}
    page = requests.get(url_year, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")   
    links = soup.find_all(class_="entry-title")
    
    for l in links:
        link = l.get_attribute_list('href')[0]
        if 'pdf' in link:
            urls.append(link)

# write all the pdf out
if not os.path.exists('pdf'):
    os.makedirs('pdf') 
for url in urls:
    random_user_agent  = random.choice(user_agents).rstrip()
    headers = {'User-Agent': random_user_agent}
    r=requests.get(url_ic3 + url, headers=headers).content
    file_name = 'pdf/' + url.split('/')[-1]
    print('writing file: ' + file_name + '')
    with open(file_name,'wb') as f:
        f.write(r)
    time.sleep(delay)
print('Done ... ... ')