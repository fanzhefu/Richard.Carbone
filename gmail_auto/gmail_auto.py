# -*- coding: utf-8 -*-
"""
Install yagmail with pip first:

pip install yagmail
"""

#!/usr/bin/env python
import yagmail

RECIPIENTS = ['fanzhefu@gmail.com', 'fanzhefu@hotmail.com',
              'zhefu.fan@forces.gc.ca', 'zhefu.fan@ecn.forces.gc.ca']

SENDER = 'ctic.cfnoc@gmail.com'
PASSCODE = '0123456789abcdef'  # a token for gmail

SUBJECT = 'Automation Test Subject'
CONTENT = ['The mail body content is here. \n \
                                              \
           Thank you',
           'attach_file1.txt', 'attach_file1.txt']  # attache files

with yagmail.SMTP(SENDER, PASSCODE) as yag:
    yag.send(RECIPIENTS, SUBJECT, CONTENT)
    print(f'Send email to {"; ".join(RECIPIENTS)} successfully')
