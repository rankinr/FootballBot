curtime=time.localtime()

if time.localtime()[5] == 0:
	user_teams={}
	if curtime[3] == 4 and curtime[4] == 0: users_in_channel=[]
	for user in users_in_channel:
		if (user.count('|') != 0 or user.count('[') != 0):
			if user.count('|') != 0: newo=user[user.find('|')+1:]
			elif user.count('[') != 0: 
				newo=user[user.find('[')+1:]
			if newo.count(']') != 0: newo=newo[:newo.find(']')]
			if newo.count('|') != 0: newo=newo[:newo.find('|')]
			if  ''.join(params).strip() == '' and newo.strip() != '': params=[newo.strip()]
			if newo.strip() != '': 
				un_team=match(newo)
				if un_team:
					if not un_team in user_teams: user_teams[un_team]=[]
					user_teams[un_team].append(user)

	

#GENERATE RANDOM USER INTERACTIONS BASED ON CURRENT GAMES
#	see if we should bother
if dlevel > db['drunksettings']['remarks']['min'] and random.randrange(0,db['drunksettings']['remarks']['randomize']) < dlevel:
	#	get the active games
	livegames=[]
	overlap=[]
	for a,b in db['games'].iteritems():
		if a != 'lastupdate':
			if b['status'].count('1ST') != 0 or b['status'].count('2ND') != 0 or b['status'].count('3RD') != 0 or b['status'].count('4TH') != 0 or b['status'].count('HALFTIME') != 0:
				livegames.append(b['team1'])
				livegames.append(b['team2'])
	for team_l in [x.lower() for x in livegames]:
		if team_l in user_teams: overlap.append(team_l)
	if len(overlap) > 0:
		team_target=random.choice(overlap)
		thegame=False
		for a,b in db['games'].iteritems():
			if a != 'lastupdate':
				if b['team1'].lower() == team_target or b['team2'].lower()==team_target: thegame=b
	if thegame != False:
		user_target=random.choice(user_teams[team_target])
		game_status='unknown'
		if thegame['team1'].lower()==team_target:
			if int(thegame['team1score']) > int(thegame['team2score']):
				if int(thegame['team1score'])-int(thegame['team2score']) > 20: game_status='winning_much'
				else: game_status='winning_little'
			elif int(thegame['team2score']) > int(thegame['team1score']):
				if int(thegame['team2score'])-int(thegame['team1score']) > 20: game_status='losing much'
				else: game_status='losing_little'
			elif int(thegame['team2score']) == int(thegame['team1score']): game_status='tied'
		elif thegame['team2'].lower()==team_target:
			if int(thegame['team1score']) > int(thegame['team2score']):
				if int(thegame['team1score'])-int(thegame['team2score']) > 20: game_status='losing_much'
				else: game_status='losing_little'
			elif int(thegame['team2score']) > int(thegame['team1score']):
				if int(thegame['team2score'])-int(thegame['team1score']) > 20: game_status='winning_much'
				else: game_status='winning_little'
			elif int(thegame['team2score']) == int(thegame['team1score']): game_status='tied'
		if game_status != 'unknown': 
			db['msgqueue'].append([random.choice(db['language'][game_status]).replace('%USER%','*'+user_target+'*'),'#redditcfb'])
		#team_target, thegame, user_target