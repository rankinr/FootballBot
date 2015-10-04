import urllib,urlparse,time,random,re,traceback
import os,json
from bs4 import BeautifulSoup
from mechanize import Browser
startingat=time.time()
from collections import OrderedDict
from HTMLParser import HTMLParser


exec(open('/home/fbbot/cfb/sload.py').read())
teams=json.loads(sql.unique_get('data','teams'))
players=[]
for team,tid in teams.iteritems():
	print team
	page=BeautifulSoup(urllib.urlopen('http://espn.go.com/college-football/team/stats/_/id/'+tid).read(),'html5lib')
	for row in page.findAll('tr',{'class':['oddrow','evenrow']}):
		if row.getText().count('statistics available') == 0:
			player=row.find('td')
			if player.a['href'] != None: player_url=player.a['href']
			else: player_url=''
			player_name=player.getText()
			par=[player_name,player_url,team]
			if not par in players: players.append(par)
open('/home/fbbot/cfb/players.list','w').write(json.dumps(players))