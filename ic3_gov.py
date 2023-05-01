# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:35:42 2023

@author: fan.z
"""
#/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import time

# News | CISA
url_ic3 = "https://www.ic3.gov"
years = [2020,2021,2022,'Current']  # read from the website

# the url of all the links
urls = []
for year in years:
    url_year= url_ic3 + '/Home/IndustryAlerts?pressReleasesYear=_' + str(year)
    page = requests.get(url_year)
    soup = BeautifulSoup(page.content, "html.parser")   
    links = soup.find_all(class_="entry-title")
    
    for l in links:
        link = l.get_attribute_list('href')[0]
        if 'pdf' in link:
            urls.append(link)

# write all the pdf 
for url in urls:
    r=requests.get(url_ic3 + url).content
    file_name = url.split('/')[-1]
    print('writing file: ' + file_name + '')
    with open(file_name,'wb') as f:
        f.write(r)

print('Done ... ... ')