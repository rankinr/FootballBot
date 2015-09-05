import urllib, urlparse, time, random, re, traceback
import os, fcntl, json
from BeautifulSoup import BeautifulSoup
from mechanize import Browser


def mrsc(gid):
    mech = Browser()
    url = "http://espn.go.com/ncf/playbyplay?gameId=" + gid + "&period=0"
    page = mech.open(url)
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.findAll("table")[-1]
    rows = table.findAll('tr')[::-1]
    c = 0
    toret = ''
    keepgoing = True
    while c < 10 and keepgoing and c < len(rows):
        cols = rows[c].findAll('td')
        #print rows[c]
        if len(cols) > 2:
            if str(cols[2]) != '<td>&nbsp;</td>' and str(
                    cols[3]) != '<td>&nbsp;</td>' and str(rows[c]).count(
                            '<span class="bi">') != 0:
                toret = str(' '.join(cols[1].findAll(text=True)))
                keepgoing = False
        c = c + 1
    return toret


mrsc('332780087')
