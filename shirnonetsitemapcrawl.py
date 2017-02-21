# -*- coding: utf-8 -*-

import base64
import gzip

import requests
from lxml import html
import xml
import os

BASE_OUTPUT_DIR = os.environ.get("BASE_OUTPUT_DIR")
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Upgrade-Insecure-Requests': "1",
    'Cookie': '__gads=ID=c72035c38130c01a:T=1479156596:S=ALNI_Ma2Lu3GNDr6cONvbo2KxjzrWQayaQ; tools=s%3ASw8aLdGdPZuuG26nPwREa6q9GBa0JgQT.s7p0ij3SbuvluAtXhMkCOXp2c59b2CmFM9lluD8UVdM; uniqueId=e27df666-11ed-890c-8d24-5bd403cfa024; WoGesacoZUa=35Up"6_iolW1FdHazhQG1cVFnTAWsLBKeBxSzFGDozw9Oxyl1OlO4awAxS_d-huPh5a; JSESSIONID=29542AACBAAB776897B02886693162D4; _ga=GA1.3.869967510.1451589715; _ga=GA1.4.869967510.1451589715; rbzid=a283ZzFtWkJxRjBHUTI3cTNLeDd3WjRzSHNRdFNhblphRVFxcW1yTnowOTRCeG8zM3c1MU54SHhUckRiK0dQT2hRREE0bzM0SUFEVUc3Qk9Za2FUR1J3QWxsSTcvVXpzTlNjRGpUR2J5bVh0azdMSHkrMnoyYUtHOHhXRTNraUFWR1NsKzhtT0lSbDZHM1BETE55Yk1heW1xcUg1MHJxWUFoL2k2LzYxZTIzNUY5V3U2c2hvaVpPb3RzY2c3cTJtUHczOTU3UGNSWjVLZGUrblo2UUVFM2Zjbi91M08zd2QrakxZaE9DdHhDST1AQEAyQEBALTE0ODE0ODE0Njgw'
}

import requests

from bs4 import BeautifulSoup

cidx = ord('א') - 144


def parse_to_str(bs):
    strlist = []
    idx = 0
    while idx < len(bs):
        if bs[idx] in [194, 215]:
            idx += 1
            strlist.append(chr(cidx + bs[idx]))
        else:
            strlist.append(chr(bs[idx]))
        idx += 1
    return ''.join(strlist).replace('\r', '\n')


def parse_sitemap(url):
    resp = requests.get(url, headers=headers)

    # we didn't get a valid response, bail
    if 200 != resp.status_code:
        return False

    # BeautifulStoneSoup to parse the document
    soup = BeautifulSoup(gzip.decompress(resp.content), "lxml")

    # find all the <url> tags in the document
    urls = soup.findAll('url')

    # no urls? bail
    if not urls:
        return False

    # storage for later...
    out = []

    # extract what we need from the url
    for u in urls:
        loc = u.find('loc').string
        resp = requests.get(loc, headers=headers)
        lyricbytes = ' '.join(html.fromstring(resp.text).xpath('.//span[@class="artist_lyrics_text"]/text()')).replace(
            b'\xc3\x97'.decode(), '').encode()
        print(loc)
        print(parse_to_str(lyricbytes))
        # fname = base64.b64encode(loc.encode()).decode()
        # with open(os.path.join(BASE_OUTPUT_DIR, 'shironet', fname), 'w') as f:
        #     f.write(resp.content)
    return out


if __name__ == '__main__':
    # parse_sitemap('http://shironet.mako.co.il/sitemap.xml')
    parse_sitemap("http://shironet.mako.co.il/Sitemap/works_heb_1.xml.gz")
