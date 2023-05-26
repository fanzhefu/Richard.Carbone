__author__ = "Mandiant"
___version___ = "1.04"

# import hashlib
# import hmac
# import email
# import time
# import datetime
# import xlsxwriter
# import threading
# import traceback
# import sys
import os
import json
import requests
from requests.auth import HTTPBasicAuth


THREATACTOR_FILE = 'threatactors.txt'
threatactors = []

#indicators = []
#threadLimiter = threading.BoundedSemaphore(100)
v4_URL = 'https://api.intelligence.mandiant.com'
v4_public_key = '89635eb99d9f8fc1f3ad9e2e5c81eb9584346fb7f6e7f30e2b9e2684bef17966'
v4_private_key = '22f8b00152b542aa101d75f38dbfb097558aaff11fc65b14278261ea16013789'

with open(THREATACTOR_FILE, 'r', encoding='utf-8') as f:
    threatactors = f.readlines()
if not os.path.exists('json'):
    os.makedirs('json')
if not os.path.exists('txt'):
    os.makedirs('txt')

def parseIndicators(actorArray):
    for actor in actorArray:
        indent_actor = json.dumps(actor, indent=2)
        # print (indent_actor)
        with open(fname_json, "a", encoding="utf-8") as f:
            f.write(f"{indent_actor}" + '\n')

for threatactor in threatactors:
    actor_id = threatactor.rstrip().split(',')[0]
    actor_name = threatactor.rstrip().split(',')[1].strip()
    fname_json = 'json\\APIv4_' + \
        actor_name.replace(" ", "_") + '_Actor_Attack_Patterns.json'
    fname_txt = 'txt\\APIv4_' + \
        actor_name.replace(" ", "_") + '_Actor_Attack_Patterns.txt'

    accept_header = 'application/json'
    x_app_name = 'APIv4_' + actor_name + 'Actor_Attack-Patterns'
    headers = {
        'Content-Type': accept_header,
        'Accept': accept_header,
        'X-App-Name': x_app_name,
        'charset': 'utf-8'
    }
    authorization = HTTPBasicAuth(v4_public_key, v4_private_key)
    payload = {}
    ENDPOINT = 'https://api.intelligence.mandiant.com/v4/actor/' + \
        actor_name + '/attack-pattern'
    print(ENDPOINT)
    response = requests.request(
        "GET", ENDPOINT, headers=headers, data=payload, auth=authorization)

    parseIndicators(response.json()['threat-actors'])
    data = json.dumps(response.json())
    data_2 = json.dumps(data, indent=2)

    with open(fname_txt, "a", encoding="utf-8") as f:
        f.write(data_2)

print("\nAll Done, check results at folders "txt" and "json" ... ...")
