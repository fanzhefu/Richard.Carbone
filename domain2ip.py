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
    """
    parser = argparse.ArgumentParser(
        description = '''The purpose of this python snippet is to convert Domain to IP.''', epilog = '''All rights reserved, CTIK CFNOK''')
    parser.add_argument("-d", "--domain", metavar='domain-file', type=str, help="The input domain file name, default=domain_list.txt",
                        nargs='?', default='domain_list.txt', const='domain_list.txt')
    parser.add_argument("-i", "--ip", metavar='ip-file', type=str, help="The output ip file name, default=ip_from_domain_list.txt",
                        nargs='?', default='ip_from_domain_list.txt', const='ip_from_domain_list.txt')
    parser.add_argument("-o", "--output", metavar='output-file', type=str, help="The output domain-ip paire file name, default=domain_ip.txt",
                        nargs='?', default='domain_ip.txt', const='domain_ip.txt')
    args = parser.parse_args()
    return args

def main(domain_file_name, ip_file_name, domain_ip_file_name):
    # opening and reading the file
    with open(domain_file_name, encoding="utf8") as domain_file:
        domains = domain_file.readlines()
        
    # initializing the list object
    ip_list = [] # extracted ip address 
    domain_ip_dict = {} # extracted domain names 
    
    for domain in domains:
        # print(domain,end= ':')
        try:
            ip = socket.gethostbyname(domain.strip())
        except socket.gaierror:
            ip = ''
        # print('ip',ip)
        ip_list.append(ip)
        domain_ip_dict[domain.strip()] = ip
        # print(domain,ip)
    #Output into files
    with open(ip_file_name, 'w', encoding="utf8") as ip_list_file:
         ip_list_file.writelines("%s\n" % ip for ip in list(set(ip_list)))
    
    # print(domain_list)
    with open(domain_ip_file_name, 'w', encoding="utf8") as domain_ip_file:
        domain_ip_file.writelines("%s:%s\n" % (key, value) for key, value in domain_ip_dict.items() )

if __name__ == "__main__":
    domain_file_name, ip_file_name, domain_ip_file_name = parse_args().domain, parse_args().ip, parse_args().output
    for i in tqdm(range(100), desc = 'Processing...'):
        main(domain_file_name, ip_file_name, domain_ip_file_name)
