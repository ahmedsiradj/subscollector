
import requests
from bs4 import BeautifulSoup
import os
import re
import json
import threading
import argparse
from colored import fg,attr
import sys



class subscollector:
    def __init__(self,domain,output,verbose):
        self.domain = domain
        self.subdomains = []
        self.output = output
        self.verbose = verbose

        main_func = threading.Thread(target=self.run())
        main_func.start()
        main_func.join()



        if(self.verbose):
            self.display()

        if(self.output):
            self.write()

    def run(self):

        func1 = threading.Thread(target=self.rapiddns(self.domain))
        func2 = threading.Thread(target=self.cth(self.domain))
        func3 = threading.Thread(target=self.whoisxmlapi(self.domain))

        func1.start()
        func2.start()
        func3.start()

        func1.join()
        func2.join()
        func3.join()

        self.subdomains = list(set(self.subdomains))

    def rapiddns(self,domain):
        page = requests.get(f"https://rapiddns.io/subdomain/{domain}#result")
        soup = BeautifulSoup(page.content,'lxml')
        list = soup.find_all(string=re.compile(f"([a-zA-Z]|[-])\.{domain}"))
        self.subdomains.extend(list)



    def cth(self,domain):
        page = requests.get(f"https://crt.sh/?q={domain}")
        soup = BeautifulSoup(page.content,"lxml")
        list = soup.find_all(string=re.compile(f"([a-zA-Z]|[-])\.{domain}"))
        self.subdomains.extend(list)



    def whoisxmlapi(self,domain):
        apikey = ""
        if(not apikey):
           return
        response = requests.get(f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={apikey}&domainName={domain}")
        data = json.loads(response.content)
        records = data["result"]["records"]
        list = [x["domain"] for x in records]
        self.subdomains.extend(list)



    def write(self):
        filename = os.path.basename(self.output)
        dirname = os.path.dirname(self.output)
        if not os.path.exists(dirname):
            print("[-] Invalid output: " + dirname)
            exit()
        os.chdir(dirname)
        file = open(filename,"w")
        for sub in self.subdomains:
            file.write(sub + "\n")
        file.close()

    
    
    
    def display(self):
        for subdomain in self.subdomains:
            print(subdomain)



    

if __name__ == "__main__":

    print(f'''{fg(159)}{attr(1)}
                       _____       __                    ____          __            
                      / ___/__  __/ /_  ______________  / / /__  _____/ /_____  _____
                      \__ \/ / / / __ \/ ___/ ___/ __ \/ / / _ \/ ___/ __/ __ \/ ___/
                     ___/ / /_/ / /_/ (__  ) /__/ /_/ / / /  __/ /__/ /_/ /_/ / /    
                    /____/\__,_/_.___/____/\___/\____/_/_/\___/\___/\__/\____/_/     

                                                                Version: 1.0
                                                                Created By: @Siradj
                                                                Github: github.com/ahmedsiradj
                    
                    {fg(15)}{attr(1)}''')





    parser = argparse.ArgumentParser(description='Subdomains Enumeration')

    parser.add_argument('-d', '--domain', required=True)
    parser.add_argument('-o', '--output', required=False, default=None)
    parser.add_argument('-v','--verbose',action="store_true",help="To display the output",required=False)
    args = parser.parse_args()
    if sys.argv[2] == "-h" or sys.argv[2] == "--help":
        parser.print_help()
        exit()

    subscollector(args.domain,args.output,args.verbose)
