import urllib,json, urllib2
from oauth2client.client import flow_from_clientsecrets
from bs4 import BeautifulSoup
exec(open('/home/fbbot/cfb/sload.py').read())
exec(open('/home/fbbot/cfb/common_functions.py').read())

teams_ranks={}
def rcfbProcess(week):
	p=week+96 # will have to adjust in future seasons
	ap=BeautifulSoup(urllib.urlopen('http://rcfbpoll.com/current-rankings.php?p='+str(p)),"html.parser")
	ap_table=ap.find('table')
	rows=ap_table.findAll('tr')
	if len(rows) == 0: 
		teams_ranks['last_week']=week-1
		return False
	else:
		for row in rows:
			col=row.findAll('td')
			team=col[1].findAll('a')[1].getText()
			if not team in teams_ranks: teams_ranks[team]={}
			teams_ranks[team][str(week)]=col[0].getText()
		return True
go=True
c=0
while go:
	c+=1
	go=rcfbProcess(c)
	if c > 20: go=False
sql.unique_set('data','all_ranks',json.dumps(teams_ranks))