# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:36:07 2023

@author: fan.z
"""
#!/usr/bin/env python
import os
import sys
import time
import random
import requests
from bs4 import BeautifulSoup

# News | CISA
WEBSITE = "https://www.cisa.gov"
PAGES = 61  # get THIS NUMBER from the website
# PAGES = 2  # for testing
DELAY = 5  # seconds
TIMEOUT = 2

# read all user agents in
if os.path.exists('user-agents.txt'):
    USER_AGENTS = open('user-agents.txt', 'r', encoding='utf-8').readlines()
else:
    print('user-agents.txt file not found, download the file here from \
          https://github.com/fanzhefu/luna.thecat/tree/main/common-files')
    sys.exit()

# store the links of all the aticles
urls = []
# The website connection check, and scarp all the links
try:
    #r = requests.get(WEBSITE, timeout=TIMEOUT, verify=True)
    # r.raise_for_status()
    if os.path.exists('links_news.txt'):
        urls = [url.rstrip()
                for url in open('links_news.txt', 'r', encoding='utf-8').readlines()]
    else:
        print('scraping all the links ... ... ')
        for page in range(PAGES):
            url_page = WEBSITE + '/news-events/news?page=' + str(page)
            random_user_agent = random.choice(USER_AGENTS).rstrip()
            headers = {'User-Agent': random_user_agent}
            page = requests.get(url_page, headers=headers, timeout=TIMEOUT)
            soup = BeautifulSoup(page.content, "html.parser")
            titles = soup.find_all(class_="c-teaser__title")

            # for i in range(len(titles)):
            #    urls.append(titles[i].find("a")['href'])
            for i, title in enumerate(titles):
                urls.append(title.find("a")['href'])
        print('links scraping done !!!' + '\n')

except requests.exceptions.HTTPError:
    print("HTTP Error. Check the website manually.")
    sys.exit()
except requests.exceptions.ReadTimeout:
    print("Time out. Check your network connection.")
    sys.exit()
except requests.exceptions.ConnectionError:
    print("Connection error. Check your network")
    sys.exit()
except requests.exceptions.RequestException:
    print("Exception request... ...")
    sys.exit()


if not os.path.exists('news'):
    os.makedirs('news')
# loop through the urls and get the title, released date and auther of the
# article, then save into a file, sleep delayed seconds between two connections
# to slow down this process.
count = 0
#scraped = []
for url in urls:
    print(str(count) + ' of ' + str(len(urls)) + '\nreading from: ' + url + '')
    random_user_agent = random.choice(USER_AGENTS).rstrip()
    headers = {'User-Agent': random_user_agent}
    try:
        page = requests.get(WEBSITE + url, headers=headers, timeout=TIMEOUT)
        print('status_code: ', page.status_code)
        if page.status_code != 200:
            continue
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception:
        with open('links_news.txt', 'w', encoding='utf-8') as f:
            f.writelines('\n'.join(urls[urls.index(url):]))
        print('Connection problem, try again later ...')
        sys.exit()

    title = soup.find_all(class_="c-page-title__title")[0].text.strip()
    writer = soup.find_all(class_="c-page-title__author")
    author = '' if not writer else writer[0].text.strip()
    article = soup.find_all(class_="c-field__content")
    content = article[-1].text
    released = '' if len(article) == 1 else article[-2].text

    file_name = 'news/' + url.split('/')[-1] + '.txt'
    print('writing file: ' + file_name + '\n')
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(title + '\n' + author + '\n' + released + '\n' + content)
    time.sleep(DELAY)  # slow down, otherwise your ip will be blocked
    count += 1

if os.path.exists("links_news.txt"):
    os.remove("links_news.txt")

print('All done ... ... ')
