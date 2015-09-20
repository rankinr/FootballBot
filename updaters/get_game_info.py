import urllib, json

def getGameInfo(typ):
	scoreboard=urllib.urlopen('http://espn.go.com/college-football/scoreboard/_/group/'+typ+'/year/2015/seasontype/2/').read()
	scoreboard=scoreboard[scoreboard.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):]
	scoreboard=json.loads(scoreboard[:scoreboard.find('}};')+2])
	games={}
	for event in scoreboard['events']:
		this_game={}
		this_game['team1']=event['competitions'][0]['competitors'][0]['team']['location']
		this_game['team1score']=event['competitions'][0]['competitors'][0]['score']
		this_game['team2']=event['competitions'][0]['competitors'][1]['team']['location']
		this_game['team2score']=event['competitions'][0]['competitors'][1]['score']
		hometeam=''
		this_game['neutral']=True
		if event['competitions'][0]['competitors'][0]['homeAway']=='home':
			this_game['hometeam']=this_game['team1']
			this_game['neutral']=False
		elif event['competitions'][0]['competitors'][1]['homeAway']=='home':
			hometeam=this_game['team2']
			this_game['neutral']=False
		this_game['gid']=event['id']
		if 'weather' in event and 'temperature' in event['weather']: this_game['temperature']=event['weather']['temperature']
		else: this_game['temperature']=''
		this_game['status']=event['status']['type']['shortDetail']
		games[this_game['team1']+this_game['team2']]=this_game
	return games
for a,b in getGameInfo('81').iteritems():
	if b['neutral']==True: team_disp=b['team1']+' '+b['team1score']+' vs. '+b['team2']+' '+b['team2score']
	elif b['hometeam']==b['team1']: team_disp=b['team2']+' '+b['team2score']+' @ '+b['team1']+' '+b['team1score']
	elif b['hometeam']==b['team2']: team_disp=b['team1']+' '+b['team1score']+' @ '+b['team2']+' '+b['team2score']
	if b['temperature'] != '': weather=' - Forecast: '+str(+b['temperature'])+'F'
	todisp=team_disp+' ('+b['status']+')'+weather
	todisp=todisp.encode('utf-8')
	print todisp