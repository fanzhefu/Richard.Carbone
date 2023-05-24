__author__ = "Mandiant"
___version___ = "1.04"



import hashlib
import hmac
import email
import time
import json
import requests
import datetime
from requests.auth import HTTPBasicAuth
import xlsxwriter
import threading
import traceback
import sys

indicators = []
#threadLimiter = threading.BoundedSemaphore(100)
v4_URL = 'https://api.intelligence.mandiant.com'
v4_public_key = '89635eb99d9f8fc1f3ad9e2e5c81eb9584346fb7f6e7f30e2b9e2684bef17966'
v4_private_key = '22f8b00152b542aa101d75f38dbfb097558aaff11fc65b14278261ea16013789'
actor_name = 'APT5'
actor_id = 'threat-actor--3e804fac-aeb4-5889-bd6a-3b89c981ed70'
accept_header = 'application/json'
x_app_name = 'APIv4_' + actor_name + 'Actor_Attack-Patterns'
offset = 0
payload={}
fname='APIv4_' + actor_name + '_Actor_Attack_Patterns.json'
ENDPOINT = 'https://api.intelligence.mandiant.com/v4/actor/' + actor_name + '/attack-pattern'
headers = {
    'Content-Type': accept_header,
    'Accept': accept_header,
    'X-App-Name': x_app_name,
    'charset': 'utf-8'
    }
authorization = HTTPBasicAuth(v4_public_key, v4_private_key)

def parseIndicators(actorArray):
    for actor in actorArray:
        indent_actor = json.dumps(actor, indent=2)
        print (indent_actor)
        
        with open(fname, "a", encoding="utf-8") as f:
            f.write(f"{indent_actor}" + '\n')
        
print (ENDPOINT)
response = requests.request("GET", ENDPOINT, headers=headers, data=payload, auth=authorization)

parseIndicators(response.json()['threat-actors'])

data = json.dumps(response.json())
data_2 = json.dumps(data, indent=2)
with open(fname, "a", encoding="utf-8") as f:
    f.write(data_2)
