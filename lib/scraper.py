#! /usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import requests

def scrape_indeed():
    url = 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?k=Job&c=qoz9VfwL&j=oKni1fwa&s=Indeed'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    print [x.string for x in soup.findAll('a')]

scrape_indeed()

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
