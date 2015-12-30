"""This runs every morning to get the list of networks that games will be on."""

from mechanize import Browser
from bs4 import BeautifulSoup
import json

exec(open('/home/fbbot/cfb/sload.py').read())


mech = Browser()

url = "http://espn.go.com/college-football/schedule"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)
tables = soup.findAll("table")
import re,urllib,os,fcntl,json
db={}
db['ntwks']={}
db['games']=json.loads(sql.unique_get('data','games'))
for table in tables:
	rows = table.findAll('tr')
	for row in rows:
		cols = row.findAll('td')
		if len(cols) > 0:
			if str(cols[2]).count('date_time') != 0 or str(cols[2]).count('class="live"') != 0: #I'm not actually sure why I have this here. I assume I did it for a reason.
				tvo=cols[2]
				tv=str(cols[3])
				team1=str(cols[0])
				team2=str(cols[1])
				team1=team1[team1.find('<span>')+len('<span>'):]
				team1=team1[:team1.find('</span>')].replace('&amp;','&')
				team2=team2[team2.find('<span>')+len('<span>'):]
				team2=team2[:team2.find('</span>')].replace('&amp;','&')
				ntwks=[]
				#print tv
				if tv.count('espn-abc') != 0: ntwks.append('ABC')
				if tv.count('espn-3') != 0: ntwks.append('ESPN3')
				if tv.count('espn2') != 0 or tv.count('espn-2') != 0: ntwks.append('ESPN2')
				if tv.count('espn-red') != 0: ntwks.append('ESPN')
				if tv.count('espnews') != 0: ntwks.append('ESPNEWS')
				if tv.count('logo-watchespn') != 0: ntwks.append('WATCHESPN')
				if tv.count('espn-U') != 0: ntwks.append('ESPNU')
				if tv.count('secnetwork.com') != 0: ntwks.append('SEC Network')
				if tv.count('FOX') != 0: ntwks.append('FOX')
				if tv.count('CBS') != 0: ntwks.append('CBS')
				if tv.count('NBC') != 0: ntwks.append('NBC')
				if tv.count('PAC12') != 0: ntwks.append('PAC12')
				if tv.count('BTN') != 0: ntwks.append('BTN')
				if tv.count('CBSSN') != 0: ntwks.append('CBSSN')
				if tv.count('FOXS1') != 0: ntwks.append('FOXS1')
				tvo=tvo.findAll(text=True)
				for a in tvo:
					if str(a).strip() != '' and str(a).strip() != 'LIVE': ntwks.append(str(a))
				ntwks=', '.join(ntwks)
				if len(ntwks) != 0:
					if ntwks[-1]==',': ntwks=ntwks[:-1]
				ntwks=ntwks.strip()
				daname=''
				if team1.count('bama') != 0: print team1+team2
				if team1+team2 in db['games']: daname=team1+team2
				elif team2+team1 in db['games']: daname=team2+team1
				if daname != '':
					db['ntwks'][daname]=ntwks
				if daname.count('bama') != 0: print daname+ntwks
sql.unique_set('data','ntwks',json.dumps(db['ntwks']))