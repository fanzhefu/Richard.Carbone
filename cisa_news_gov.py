# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:36:07 2023

@author: fan.z
"""

#/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import time

# News | CISA
url_cisa = "https://www.cisa.gov"
pages = 61  # get from the website
delay = 3 #seconds

# get the url of all the aticles
urls = []
for page in range(pages):
    url_page = url_cisa + '/news-events/news?page=' + str(page)
    page = requests.get(url_page)
    soup = BeautifulSoup(page.content, "html.parser")   
    titles = soup.find_all(class_="c-teaser__title")
    
    for i in range(len(titles)):
        urls.append(titles[i].find("a")['href'])

# loop through the urls and get the title, released date and auther of the article,
# then save into a file, sleep delayed seconds between two connections to slow down this process. 
for url in urls:
    status_code = 0
    while status_code != 200:
        page = requests.get(url_cisa + url)
        status_code = page.status_code    #warus
        if status_code != 200:
            print('status_code:', status_code)
            time.sleep(delay)   # wait for 5 seconds and retry
            continue
    soup = BeautifulSoup(page.content, "html.parser")   

    title = soup.find_all(class_="c-page-title__title")[0].text.strip()
    
    writer = soup.find_all(class_="c-page-title__author")
    author = '' if not writer else writer[0].text.strip()
    
    article = soup.find_all(class_="c-field__content")
    content = article[-1].text
    released = '' if len(article)==1 else article[-2].text
    
    file_name = url.split('/')[-1] +'.txt'
    print('writing file: ' + file_name + '')
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(title +'\n'+ author +'\n'+ released +'\n'+ content)
    time.sleep(delay)    #slow down, otherwise your ip will be blocked

print('Done ... ... ')
