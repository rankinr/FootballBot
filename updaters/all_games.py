from mechanize import Browser
from bs4 import BeautifulSoup

mech = Browser()

url = "http://espn.go.com/college-football/schedule"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html, "html5lib")
tables = soup.findAll("table", attrs={'class': 'schedule'})
import re, urllib, os, fcntl, json

gms = []

for tb in tables:
    date = tb.find('caption').getText().encode('utf-8')
    #print date
    games = tb.findAll('tr', {'class': ['even', 'odd']})
    for game in games:
        teams = game.findAll('a', {'class': 'team-name'})
        team1 = teams[0].getText().encode('utf-8')
        team2 = teams[1].getText().encode('utf-8')
        gms.append(date + ': ' + team1 + ' @ ' + team2)
for a in gms:
    print a
