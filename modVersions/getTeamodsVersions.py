#!/usr/bin/env python3
import re
import math
import json
import time
import random
import requests

versionRex = re.compile('Game[\s]*Version:[\s]*(([0-9]*\.){1,}[0-9]*|[forgeFORGE]{5})')

# These values are abstracted because they may need to be modified if the cookeis below become invalidated.
# To get a good copy, just open one link for a curseforge mod, and right-click "inspect" page or "developer tools".
# Get a copy of your "Cookies" header for the initial request to curseforge.com, specifically just the cloudflare ones.
# Paste that cookie string below, and copy and paste your User Agent string below
UAString = "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
CFCookies = "__cfduid=de1c20642a4f1ce9d249eeb213ad27bcd1597164214; Unique_ID_v2=117c753f7881403ba2e1052987689003; ResponsiveSwitch.DesktopMode=1; AWSALB=mY0M8agQ1yfCac0+fx5K1suYBxdC152zlntBpjHALbouVd7k8GTZCIbQHVC5OBlP7E+vucVjrrlLz/7+EZaltZ9DtjYJNlV5QxrIWjPyzUgyY3x1VEN2ILxlZhkH; AWSALBCORS=mY0M8agQ1yfCac0+fx5K1suYBxdC152zlntBpjHALbouVd7k8GTZCIbQHVC5OBlP7E+vucVjrrlLz/7+EZaltZ9DtjYJNlV5QxrIWjPyzUgyY3x1VEN2ILxlZhkH; __cf_bm=d1913713a84e86704a8e3e19fefe4ed8f2d26715-1598157873-1800-Ae2C4KMVNS75yC0HVy5OxlzJg1nLDrUhUSB0sLXlP+Dsi6LRE7MdUYFXpyR/uy00oMqI9/DBTrzETR9zrS8t6/g="

headers = {
    "User-Agent": UAString,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Cookie": CFCookies,
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "TE": "Trailers"
}

modlist = json.load(open('teamods.json', 'r'))

versionList = {}
for mod in modlist:
    req = requests.get(modlist[mod], headers=headers)
    if req.status_code < 400:
        version = versionRex.search(req.text)
        if version:
            versionList[mod] = version[1]
        else:
            versionList[mod] = req.reason
    print(mod, versionList[mod])
    time.sleep(float(math.floor(random.random()*100))/100)

with open('modvers.json', 'w+') as f:
    f.write(json.dumps(versionList, indent=4))