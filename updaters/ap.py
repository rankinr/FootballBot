from bs4 import BeautifulSoup
import json, urllib.request, time
teams={}
order=[]
ap_teams=[]
def loadUrl(url):
	try:
		local_url=url[url.find('//')+2:].replace('/','.')
		data=open(local_url,encoding='utf8').read()
	except:
		data=urllib.request.urlopen(url).read().decode('utf-8','ignore')
		open(local_url,'w',encoding='utf8').write(data)
	return data
def apProcess(ap,pre=''):
	global teams
	global order
	global ap_teams # to prevent from overwriting rankings on the second round if AP hasn't updated the others receiving votes div
	global last_week_ranks
	ap_conversions={'Mississippi':'Ole Miss', 'W. Kentucky':'Western Kentucky','Brigham Young':'BYU','Miami':'Miami (FL)','Southern Cal':'USC'}
	ap_table=ap.find('table')
	rows=ap_table.findAll('tr')
	for row in rows:
		rank=row.find('td',{'class':'trank'}).contents[0]
		team=row.find('div',{'class':'poll-team-name'})
		first_place_votes=team.getText()
		if first_place_votes.count('(') != 0:
			first_place_votes=first_place_votes[first_place_votes.find('(')+1:first_place_votes.find(')')]
		else: first_place_votes=''
		team=team.a.contents[0]
		if team in ap_conversions: team=ap_conversions[team]
		team=team.replace(' St.',' State')
		votes=row.find('div',{'class':'info-votes-wrap'}).getText().replace('Points','').strip()
		conference=row.find('div',{'class':'poll-conference'}).a.contents[0]
		record=row.find('div',{'class':'poll-record'}).contents[0]
		record=record[record.find(':')+1:].strip()
		if not team in teams:
			teams[team]={}
#			print ('No record of '+team+'. Perhaps a bye week? Or a mismatch between ESPN and AP?')
		teams[team][pre+'rank']=rank
		if pre=='last_week_': last_week_ranks[team]=rank
		teams[team][pre+'votes']=votes
		teams[team][pre+'conference']=conference
		teams[team][pre+'record']=record
		teams[team][pre+'first_place_votes']=first_place_votes
		if pre=='': order.append(team)
	ap_other=ap.find('div',{'class':'poll-footer'})
	if ap_other != None:
		ap_other=ap_other.find('p').contents[0]
		ap_other=ap_other[ap_other.find(':')+1:].strip()
		if ap_other.count(',') > ap_other.count(';'): separator=','
		else: separator=';'
		ap_other=ap_other.split(separator)
		for team_data in ap_other:
			team_data=team_data.strip()
			team=team_data[::-1]
			votes=team[:team.find(' ')][::-1].strip()
			team=team[team.find(' ')+1:][::-1].strip()
			if team.count('(') != 0:
				team=team[:team.find('(')].strip()
			if team in ap_conversions: team=ap_conversions[team]
			team=team.replace(' St.',' State')
			rank='NR'
			conference=''
			record=''
			if not team in ap_teams:
				ap_teams.append(team)
				if not team in teams: 
					print ('No record of '+team+'. Perhaps a bye week? Or a mismatch between ESPN and AP?')
					teams[team]={}
			teams[team][pre+'rank']=rank
			teams[team][pre+'votes']=votes
			teams[team][pre+'conference']=conference
			teams[team][pre+'record']=record
			if pre=='': order.append(team)
apProcess(BeautifulSoup(loadUrl('http://collegefootball.ap.org/poll/?t='+str(int(time.time()))),"html.parser"))
for team in order:
	print (team)