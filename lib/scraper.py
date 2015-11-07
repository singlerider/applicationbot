#! /usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from fake_useragent import UserAgent
import requests

ua = UserAgent() # for faking a browser
# ua.ie, ua.msie, ua['Internet Explorer'], ua.opera, ua.chrome, ua.google,
# ua['google chrome'], ua.firefox, ua.ff, ua.safari, ua.random

url = ""

def scrape(url):
    url = url
    headers = {'User-Agent': ua.chrome}
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html)
    print [x.string for x in soup.findAll('a')]

scrape(url)

"""
soup.prettify()

soup.title
# <title>The Dormouse's story</title>

soup.title.name
# u'title'

soup.title.string
# u'The Dormouse's story'

soup.title.parent.name
# u'head'

soup.p
# <p class="title"><b>The Dormouse's story</b></p>

soup.p['class']
# u'title'

soup.a
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

soup.findAll('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find(id="link3")
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
"""
