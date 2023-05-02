# -*- coding: utf-8 -*-
"""
Created on Mon May  1 18:58:02 2023

@author: fan.z
"""
#/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import os
import time

delay = 2 #seconds

url_cisa = "https://www.cisa.gov"
news_pages = 61  # get from the website
alerts_pages = 281  # get from the website


def links(pages, link):
    urls = []
    for page in range(pages):
        url_page = url_cisa + link + str(page)
        page = requests.get(url_page)
        soup = BeautifulSoup(page.content, "html.parser")   
        titles = soup.find_all(class_="c-teaser__title")
        
        for i in range(len(titles)):
            urls.append(titles[i].find("a")['href'])
    return urls

news_links = links(news_pages, '/news-events/news?page=')
for url in news_links:
    page = requests.get(url_cisa + url)
    soup = BeautifulSoup(page.content, "html.parser")   

    title = soup.find_all(class_="c-page-title__title")[0].text.strip()
    
    writer = soup.find_all(class_="c-page-title__author")
    author = '' if not writer else writer[0].text.strip()
    
    article = soup.find_all(class_="c-field__content")
    content = article[-1].text
    released = '' if len(article)==1 else article[-2].text

    if not os.path.exists('news'):
        os.makedirs('news')    
    file_name = 'news/' + url.split('/')[-1] +'.txt'
    print('writing file: ' + file_name + '')
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(title +'\n'+ author +'\n'+ released +'\n'+ content)
    time.sleep(delay)    #slow down, otherwise your ip will be blocked

alerts_links = links(alerts_pages, '/news-events/cybersecurity-advisories?page=')
for url in alerts_links:
    page = requests.get(url_cisa + url)
    soup = BeautifulSoup(page.content, "html.parser")   

    title = soup.find_all(class_="c-page-title__title")[0].text.strip()
    
    article = soup.find_all(class_="l-page-section__content")
    content = article[0].text
    
    date_and_code = soup.find_all(class_="c-field__content")
    released = 'Released: ' + date_and_code[0].text
    alert_code = '' if len(date_and_code)==1 else 'Alert Code: ' + date_and_code[1].text
    
    if not os.path.exists('alerts'):
        os.makedirs('alerts')    
    file_name = 'alerts/' + url.split('/')[-1] +'.txt'
    print('writing file: ' + file_name + '')
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(title +'\n'+ released + alert_code + content)
    time.sleep(delay)    #slow down, otherwise your ip will be blocked

print('All Done ... ... ')
