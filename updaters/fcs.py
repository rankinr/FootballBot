import urllib,urlparse,time,random,re,traceback
import os,json
from bs4 import BeautifulSoup
from mechanize import Browser
startingat=time.time()
from collections import OrderedDict
from HTMLParser import HTMLParser
exec(open('/home/fbbot/cfb/common_functions.py').read())

fcs_games=getGameInfo('81')

fcs={}

for gid, game in fcs_games.iteritems():
	fcs[gid]={}
	fcs[gid]['status']=game['status']
	fcs[gid]['team1']=game['team1']
	fcs[gid]['team2']=game['team2']
	fcs[gid]['team1score']=game['team1score']
	fcs[gid]['team2score']=game['team2score']
	fcs['hometeam']=game['hometeam']
	fcs['neutral']=game['neutral']
	fcs['ntwk']=game['network']


exec(open('/home/fbbot/cfb/sload.py').read())

sql.unique_set('data','fcs',json.dumps(fcs_games))	


"""



def isoTyp(txt,typ):
	txt=txt[txt.find('-'+typ+'"'):]
	txt=txt[txt.find('">')+2:]
	while txt[0]=='<': txt=txt[txt.find('>')+1:]
	return txt[:txt.find('<')].replace('&nbsp',' ').strip()

data={}
dtypes={'status':'statusText','ntwk':'preTV','team1':'aTeamName','team1score':'aTotal','team2':'hTeamName','team2score':'hTotal'}

while a.count('<div class="game-header">') != 0:
	a=a[a.find('<div class="game-header">')+len('<div class="game-header">'):]
	cura=a[:a.find('-leadersHeader">Game Leaders</h5>')]
	curd={}
	for b,c in dtypes.iteritems():
		curd[b]=isoTyp(cura,c)
	gid=cura[:cura.find('-statusText"')]
	gid=gid[::-1][:gid[::-1].find('"')][::-1]
	curd['gid']=gid
	data[curd['team1']+curd['team2']]=curd
	
	
	
exec(open('/home/fbbot/cfb/sload.py').read())

sql.unique_set('data','fcs',json.dumps(data))	"""