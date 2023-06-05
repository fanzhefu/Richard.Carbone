# -*- coding: utf-8 -*-
"""
Install yagmail with pip first:

pip install yagmail
"""

#!/usr/bin/env python
import yagmail

RECIPIENTS = ['fanzhefu@gmail.com', 'fanzhefu@hotmail.com',
              'fanzhefu@forces.gc.ca', 'fanzhefu@ecn.forces.gc.ca']

SENDER = 'ctic.cfnoc@gmail.com'
PASSCODE = '0123456789abcdef'  # a token for gmail

SUBJECT = 'Test Subject'
CONTENT = ['The mail body content is here',
           'attach_file1.txt', 'attach_file1.txt']  # attache files

for recipient in RECIPIENTS:
    with yagmail.SMTP(SENDER, PASSCODE) as yag:
        yag.send(recipient, SUBJECT, CONTENT)
        print('Sent email to ' + recipient + ' successfully')
print('\nAll done... ...')
