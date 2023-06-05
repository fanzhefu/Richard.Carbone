# -*- coding: utf-8 -*-
"""
chmod +x ex_ip.py
crontab -e
0 0,6,12,18 * * * /home/kali/ex_ip.py

@author: fan.z
"""

#!/usr/bin/env python

# install yagmail first
import yagmail
import requests

URL = 'http://myexternalip.com/raw'
ip = requests.get(URL).text

RECIPIENT = 'alainpetit21@hotmail.com'

SENDER = 'ctic.cfnoc@gmail.com'
PASSCODE = 'hdipeufkklgiqlir'  # a token for gmail

SUBJECT = 'external ip'
CONTENT = [f'The external ip: {ip}']

with yagmail.SMTP(SENDER, PASSCODE) as yag:
    yag.send(RECIPIENT, SUBJECT, CONTENT)
    #print(f'Send email to {RECIPIENT} successfully')
