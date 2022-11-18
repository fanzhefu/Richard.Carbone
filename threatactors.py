__author__ = "FireEye"
___version___ = "1.04"

import json
import requests
from requests.auth import HTTPBasicAuth

indicators = []
#threadLimiter = threading.BoundedSemaphore(100)
v4_URL = 'https://api.intelligence.fireeye.com'
v4_public_key = 'KEY 1'
v4_private_key = 'KEY 2'
accept_header = 'application/json'
x_app_name = 'APIv4_Actor_Reports'

# removed THREATACTOR_NAME
url = 'https://api.intelligence.fireeye.com/v4/actor/'

headers = {
    "Authorization": "HTTPBasicAuth(v4_public_key, v4_private_key)",
    "Accept": "application/json",
    "X-App-Name": "Vocabulary_downloader"
}

params = None

# read all threat actors name from file "threatactors" into THREATACTOR_NAME 
THREATACTOR_NAME = [name.strip() for name in open('threatactors', 'r').readlines()]

# loop through each threat actor
for threat_actor in THREATACTOR_NAME:
    resp = requests.get(url=url+threat_actor, headers=headers, auth=HTTPBasicAuth(v4_public_key, v4_private_key))
    print(json.dumps(resp.json(), indent=True))

