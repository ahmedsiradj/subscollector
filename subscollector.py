#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import os
import re
from datetime import date
import argparse
from colored import fg,attr
import sys


def ouput(path,subdomains):
    if path:
        filename = os.path.basename(path)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            print("[-] Invalid path: " + dirname)
            exit()
        os.chdir(dirname)
        file = open(filename,"w")
        for sub in subdomains:
            file.write(sub + "\n")
        file.close()

    else:
        for sub in subdomains:
            print(sub)

def subdomains_enumeration(domain,path):
    
    # collect subdomains from two sites
    today = date.today()
        
    # Site 1    
    page1 = requests.get(f"https://rapiddns.io/s/{domain}#result")
    soup1 = BeautifulSoup(page1.content,'lxml')
    list1 = soup1.find_all(string=re.compile(domain)) # that return a list contains subdomains from https://rapiddns.io/
    
    # Site 2
    page2 = requests.get(f"https://subdomainfinder.c99.nl/scans/{today}/{domain}")
    soup2 = BeautifulSoup(page2.content,'html.parser')
    data2 = soup2.find_all(class_="link sd")
    list2 = []
    for sub in data2:
        list2.append(sub.string) # to get the text between tags <a>...</a>
    
    # Site 3
    page3 = requests.get(f"https://crt.sh/?q={domain}")
    soup3 = BeautifulSoup(page3.content,"html.parser")
    list3 = soup3.find_all(string=re.compile(domain))

    subdomains = list(dict.fromkeys(list1 + list2 +list3))# to remove duplicate from the array

    # Handel the ouput
    ouput(path,subdomains)

    

if __name__ == "__main__":

    print(f'''{fg(159)}{attr(1)}
                       _____       __                    ____          __            
                      / ___/__  __/ /_  ______________  / / /__  _____/ /_____  _____
                      \__ \/ / / / __ \/ ___/ ___/ __ \/ / / _ \/ ___/ __/ __ \/ ___/
                     ___/ / /_/ / /_/ (__  ) /__/ /_/ / / /  __/ /__/ /_/ /_/ / /    
                    /____/\__,_/_.___/____/\___/\____/_/_/\___/\___/\__/\____/_/     

                                                                Created By: @Siradj
                                                                Github: github.com/ahmedsiradj
                    
                    ''')





    parser = argparse.ArgumentParser(description='Subdomains Enumeration')

    parser.add_argument('-d', '--domain', required=True)
    parser.add_argument('-o', '--output', required=False, default=None)
    args = parser.parse_args()
    if sys.argv[2] == "-h" or sys.argv[2] == "--help":
        parser.print_help()
        exit()
    subdomains_enumeration(args.domain,args.output)
