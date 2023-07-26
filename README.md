# subscollector

It's a python tool that used to collect subdomains from third parties `rapiddns.io`,`whoisxmlapi.com`,`crt.sh`.

## P.S.
```
You should have an api key of * [whoisxmlapi.com](https://www.whoisxmlapi.com/) * to get more results
```
### Installation:

```
git clone https://github.com/ahmedsiradj/subscollector.git
cd subscollector/
pip3 install -r requirements.txt
```

```
python subscollector.py -h
```

### Usage:

```bash
python subscollector.py -d target.com -v -o subdomains.txt
```
