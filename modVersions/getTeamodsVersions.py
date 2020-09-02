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
UAString = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
Cookies = '__cfduid=d3f82321171cc068bcdb6d98f65dd5a581598759851; Unique_ID_v2=f2472c1b117c4e8f9c1ee61db39db737; ResponsiveSwitch.DesktopMode=1; __cf_bm=3d2845d3aaf20904466b338f2e86f62fe6672345-1598760774-1800-AXX+pl+hZzGRSsEYjRq+rpvSm//XXtNu7KTofyzF8Nf7N8KLZOtDmRB7wVshJf6rcWsfDlMv8FbGrC3QlH+7U7U=; AWSALB=fwhkTCn6U+AWfjEm19+4NsBiIloeN+ai6iqVIzL3LMQiMDdE+DjmoNHOZN0ZwgG0CSK4Uh4/czwS3b8DHSaYk/eSzn3nAeI+xP3y0MhwDtHlZK1PpnBWPp6+N0gr; AWSALBCORS=fwhkTCn6U+AWfjEm19+4NsBiIloeN+ai6iqVIzL3LMQiMDdE+DjmoNHOZN0ZwgG0CSK4Uh4/czwS3b8DHSaYk/eSzn3nAeI+xP3y0MhwDtHlZK1PpnBWPp6+N0gr'

headers = {
    "user-agent": UAString,
    "cookie": Cookies,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "dnt": "1",
    "referrer": "https://www.curseforge.com/minecraft/mc-mods/adabranium",
    "upgrade-insecure-requests": "1"
}
headers = sorted(headers.items() ,  key=lambda x: x[0])
sesh = requests.Session()
sesh.headers.update(headers)
modlist = json.load(open('teamods.json', 'r'))

versionList = {}
for mod in modlist:
    req = sesh.get(modlist[mod])
    if req.status_code < 400:
        version = versionRex.search(req.text)
        if version:
            versionList[mod] = version[1]
        else:
            versionList[mod] = req.reason
        print(mod, versionList[mod])
    else:
        print("ERROR fetching {}".format(mod))
    time.sleep(float(math.floor(random.random()*100))/100)

with open('modvers.json', 'w+') as f:
    f.write(json.dumps(versionList, indent=4))