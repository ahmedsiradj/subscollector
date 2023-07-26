import requests
from bs4 import BeautifulSoup
import os
import re
import json
from datetime import date
import argparse
from colored import fg,attr
import sys

def rapiddns(domain):
    page = requests.get(f"https://rapiddns.io/subdomain/{domain}#result")
    soup = BeautifulSoup(page.content,'lxml')
    list = soup.find_all(string=re.compile(f"([a-zA-Z]|[-])\.{domain}"))



def cth(domain):
        page = requests.get(f"https://crt.sh/?q={domain}")
        soup = BeautifulSoup(page.content,"lxml")
        list = soup.find_all(string=re.compile(f"([a-zA-Z]|[-])\.{domain}"))



def whoisxmlapi(domain):
    apikey = "at_7pSkMpfVvz5lL7kUPAu0Q8Phd8SFc"
    response = requests.get(f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={apikey}&domainName={domain}")
    data = json.loads(response.content)
    records = data["result"]["records"]
    list = [x["domain"] for x in records]
    
    
    

target = "moonpay.com"

# rapiddns(target) Done

# cth(target) Done


#whoisxmlapi(target) 

