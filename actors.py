# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 09:01:22 2022

this snippet is used to 
1.scrapping https://malpedia.caad.fkie.fraunhofer.de/actors
   to get actor's name, aka, synonym, and the link to the description page.
2. go through each description page to extract actor's description'
3. write all actor's name, aka, synonym and description to actors.json file.
@author: fan.z

"""
import requests
from bs4 import BeautifulSoup
import json

URL = "https://malpedia.caad.fkie.fraunhofer.de"
ACTORS = 'actors'

page = requests.get(URL+'/'+ACTORS)
soup = BeautifulSoup(page.content, "html.parser")   

names = [name.text for name in soup.find_all(class_="common_name")]
akas = [ aka['title'].lstrip('aka: ') if (aka := row.find(class_='fa fa-info-circle')) != None else 'aka: N/A' for row in soup.find_all(class_="clickable-row")]
synonyms = [ (synonym:= row.find(class_='synonyms')).text  for row in soup.find_all(class_="clickable-row")]
links = [URL+link['data-href'] for link in soup.find_all( class_="clickable-row")]

i, total = 0, len(names) #just a counter 
descriptions = []
print(f"\nThere are total {total} acotors, it will take time, wait until done ... ...\n")
for link in links:
    # go through each page to extract the description 
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")   
    descriptions.append(soup.body.find_all(class_="col-xl-12")[1].select("p")[0].text.strip())
    print(i, end=',')
    i += 1
    
actors =[{'name':name, 'aka':aka, 'synonym':synonym, 'description':description} for (name, aka, synonym, description) in list( zip(names, akas, synonyms, descriptions) ) ]       

with open('actors.json', 'w', encoding='utf-8', newline='\r\n') as f:
    json.dump(actors, f, ensure_ascii=False, indent=4) #
    
print("\n\nDone, check output file: actors.json ... ...")
