# -*- coding: utf-8 -*-
"""
The purpose of this python snippet is to extract IP/Domain from URLs.

fan.z
"""
# importing the module
import re
import socket
import urllib.parse
import argparse
from tqdm import tqdm

def parse_args():
    """Handle the command line arguments.
    Returns:
    url_file_name, ip_file_name, domain_file_name
    """
    parser = argparse.ArgumentParser(
        description = '''The purpose of this python snippet is to extract IP/Domain from URLs.''',                    
        epilog = '''All rights reserved, CTIK CFNOK''')
    
    parser.add_argument("-u", "--url", metavar='url-file', type=str, help="The input urls file name, default=urls.txt",
                        nargs='?', default='urls.txt', const='urls.txt')
    parser.add_argument("-i", "--ip", metavar='ip-file', type=str, help="The output ip file name, default=ip_list.txt",
                        nargs='?', default='ip_list.txt', const='ip_list.txt')
    parser.add_argument("-d", "--domain", metavar='domain-file', type=str, help="The output domain file name, default=domain_list.txt",
                        nargs='?', default='domain_list.txt', const='domain_list.txt')
    args = parser.parse_args()
    return args

def main(url_file_name, ip_file_name, domain_file_name):
    # opening and reading the file
    #lines = open('URLS.txt', encoding="utf8").readlines()
    try:
        with open(url_file_name, encoding="utf8") as url_file:
            lines = url_file.readlines()
    except EnvironmentError:
        print("Check file name and location.")
        exit(1)
    # declaring the regex pattern for IP addresses
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    # domain_pattern = re.compile("^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}$")
    
    # initializing the list object
    ip_list = [] # extracted ip address 
    domain_list = [] # extracted domain names 
    
    # extracting the IP addresses and domain names from urls
    for line in lines:
        if ip_pattern.search(line) != None:
            ip_list.append(ip_pattern.search(line)[0])
        else:
            domain_name = urllib.parse.urlparse(line).netloc
            domain_list.append(domain_name)
        
    #Output into files
    with open(ip_file_name, 'w', encoding="utf8") as ip_list_file:
         ip_list_file.writelines("%s\n" % ip for ip in list(set(ip_list)))
    
    # print(domain_list)
    with open(domain_file_name, 'w', encoding="utf8") as domain_list_file:
        domain_list_file.writelines("%s\n" % domain for domain in list(set(domain_list)))
    
if __name__ == "__main__":
    
    url_file_name, ip_file_name, domain_file_name = parse_args().url, parse_args().ip, parse_args().domain
    main(url_file_name, ip_file_name, domain_file_name)