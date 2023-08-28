# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 12:34:43 2023

@author: Zhefu
"""

# https://medium.com/@sdoshi579/to-read-emails-and-download-attachments-in-python-6d7d6b60269
# https://www.geeksforgeeks.org/python-fetch-your-gmail-emails-from-a-particular-user/
# Importing libraries
'''
con.list()
Out[12]: 
('OK',
 [b'(\\HasNoChildren) "/" "INBOX"',
  b'(\\HasChildren \\Noselect) "/" "[Gmail]"',
  b'(\\All \\HasNoChildren) "/" "[Gmail]/All Mail"',
  b'(\\Drafts \\HasNoChildren) "/" "[Gmail]/Drafts"',
  b'(\\HasNoChildren \\Important) "/" "[Gmail]/Important"',
  b'(\\HasNoChildren \\Sent) "/" "[Gmail]/Sent Mail"',
  b'(\\HasNoChildren \\Junk) "/" "[Gmail]/Spam"',
  b'(\\Flagged \\HasNoChildren) "/" "[Gmail]/Starred"',
  b'(\\HasNoChildren \\Trash) "/" "[Gmail]/Trash"'])
'''
import os
import imaplib
import email

USER = 'ctic.cfnoc@gmail.com'
PASSWORD = 'hdifeupkklgiqlir'
IMAP_URL = 'imap.gmail.com'
OUTPUT_DIR = '.'
LABEL = 'Inbox'
#LABEL = '"[Gmail]/Sent Mail"'
SEARCH_KEY = 'subject'
SEARCH_VALUE = 'IOCS'


def get_body(msg):
    # Function to get email content part i.e its body part
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    return msg.get_payload(None, True)


def search(key, value, conn):
    # Function to search for a key value pair
    result, data = conn.search(None, key, '"{}"'.format(value))
    return data


def get_emails(result_bytes):
    # Function to get the list of emails under this label
    msgs = []  # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs


# this is done to make SSL connection with GMAIL
con = imaplib.IMAP4_SSL(IMAP_URL)
# logging the user in
con.login(USER, PASSWORD)
# calling function to check for email under this label
con.select(LABEL)

# searches from mail with filters like from, to or subject of mail to be found
# result is id’s of all the found emails.
mail_ids = search(SEARCH_KEY, SEARCH_VALUE, con)

i = 0 # index the number of files
for mail_id in mail_ids[0].split():
    typ, data = con.fetch(mail_id, '(RFC822)')
    raw_email = data[0][1]
    # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # downloading attachments
    for part in email_message.walk():
        # this part comes from the snipped ...
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = f"{i:04}" +'_'+ part.get_filename() 
        #to avoid identical file names
        if bool(fileName):
            filePath = os.path.join(OUTPUT_DIR, fileName)
            if not os.path.isfile(filePath):
                with open(filePath, 'wb') as fp:
                    fp.write(part.get_payload(decode=True))
                #fp.close()
            subject = str(email_message).split(
                "Subject: ", 1)[1].split("\nTo:", 1)[0]
            print(f'Downloaded "{fileName}" from email titled "{subject}"')
        i += 1
print('\nWell done... ')