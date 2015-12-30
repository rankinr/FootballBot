"""
Place a bet on <team>. You must be authorized to NickServ to issue this command. (Type /ns help for more information.) Please be aware that wallet values do not represent real money and there is no promise of a prize for winning (besides, of course, eternal IRC glory). Credit for idea to Dublock.
Users start with $100 and receive an additional $50 every week. Funds are deducted from your wallet immediately when you place the bet, and are immediately returned, along with 100% winnings, when the team you bet on covers the spread. New bets can be immediately placed with the winnings.
To place a bet that <team> will cover the spread: !bet <team> <bet> (if a bet already exists, this will overwrite the existing bet)
To cancel a bet: !bet cancel <team> <bet>
To list your information, including cash on hand and your pending bets: !bet list OR !bet me
To list rankings: !bet rank OR !bet rankings
"""
o_orig=origin
origin=origin.lower()
#db['bets']=dict((k.lower(), v) for k,v in db['bets'].iteritems())
#db['cash']=dict((k.lower(), v) for k,v in db['cash'].iteritems())
#sql.unique_set('data','bets',json.dumps(db['bets']))
#sql.unique_set('data','cash',json.dumps(db['cash']))
#print db['cash']



team_list=[]
for t in db['teams']: team_list.append(t.lower())
if dest.lower()=='footballbot': msg_dest=origin
else: msg_dest=dest
msg_type='PRIVMSG'
print '1'
def betting_ranks(csh,num): # cash = cash variable, num = number of ranks to list OR user to get rank of
	csh.pop('base!')
	sorted_csh = sorted(csh.items(), key=operator.itemgetter(1))
	sorted_csh.reverse()
	try:
		num=float(num)
		c=0
		c_last=c
		csh_last=0
		r_list=[]
		while c < num and c < len(sorted_csh):
			c+=1
			if csh_last != sorted_csh[c-1][1]: c_last=c # for ties
			csh_last=sorted_csh[c-1][1]
			r_list.append(str(c_last)+'. '+sorted_csh[c-1][0]+' ('+cashVal(sorted_csh[c-1][1])+')')
		return ' | '.join(r_list)
	except:
		if num in csh:
			c=0
			c_last=c
			csh_last=0
			cont=True
			while cont and c < 10000:
				c+=1
				if csh_last != sorted_csh[c-1][1]: c_last=c # for ties
				csh_last=sorted_csh[c-1][1]
				if sorted_csh[c-1][0]==num: cont=False
			return str(c_last)
		else: return False
if params[0]=='me' or params[0]=='list':
	if origin in db['bets'] and origin in db['cash']:
		msg=o_orig+', you have $'+cashVal(db['cash'][origin])+' in your wallet and are ranked #'+betting_ranks(db['cash'],origin)+' out of '+str(len(db['cash']))+' participants.'
		active_bets=[]
		for a,b in db['bets'][origin].iteritems():
			if a in db['games_new']['fbs']: active_bets.append('$'+cashVal(b[2])+' on '+b[0]+' '+b[1]+' ('+db['games_new']['fbs'][a]['team1']+' vs '+db['games_new']['fbs'][a]['team2']+')') #team, spread, bet value
		msg+=' Your active bets: '+' | '.join(active_bets)
		for m in splitMessage(msg, 450,'|'): db['msgqueue'].append([m,msg_dest,msg_type])
	else:
		db['msgqueue'].append(['Oops! For some reason I don\'t have a record of you.',msg_dest,msg_type])
elif params[0] == 'rank' or params[0]=='rankings' or params[0]=='ranks':
	n=10
	if len(params) > 1:
		try:
			n=float(params[1])
		except: n=10
	if n > 30: n=30
	for m in splitMessage('Betting game rankings: '+betting_ranks(db['cash'],n),450,'|'): db['msgqueue'].append([m,msg_dest,msg_type])
elif auth(origin,line):
	if not origin in db['cash']: db['cash'][origin]=db['cash']['base!']
	try:
		bet=float(params[0].replace('$','').strip())
		team=params[1:]
	except:
		try: 
			bet=float(params[-1].replace('$','').strip())
			team=params[:-1]
		except: bet=False
	cancel=False
	if ' '.join(params).lower().count('cancel') != 0:
		team=' '.join(params).lower().replace('cancel','').replace('  ',' ').strip().split(' ')
		cancel=True
	#GET THE GAME
	print bet
	print team
	
	if bet or cancel:
		bye=False
		closest_bye_alt=''

		short_params=''.join(team).lower().replace(' ','')
		if short_params in abbrev_lower:
			team=abbrev_lower[short_params].split(' ')
			short_params=''.join(team).lower().replace(' ','')

		if ''.join(team).strip() != '':
			tbyname={}
			closestval=1000000
			closests=''
			teams=db['games_new']['fbs'].copy()
			team=' '.join(team).lower()
			params_orig=team
			if not team in team_list: params=abbrev(team,db['abbreviations'])
			for a,b in teams.iteritems():
				if a != 'lastupdate':
					team1=b['team1'].lower().replace('(','').replace(')','')
					team2=b['team2'].lower().replace('(','').replace(')','')
					if team.count(' ') == 0: tclv=closest([params_orig,team.lower(),team.lower()+' StateZ',team.lower().replace('st','state')],[team1.lower(),team2.lower()])
					else: tclv=closest([params_orig,team.lower(),team.lower().replace('st','state')],[team1.lower(),team2.lower(),team1.lower()+team2.lower(),team2.lower()+team1.lower()])
					if tclv < closestval:
						closestval=tclv
						closests=a

			if closestval != 0 and params_orig in team_list:
				bye=True
				team=params_orig
				closests=''
			print closests
			print closestval
			if (closests != '' and closestval <= 3 and not isAutoDetect) or (closests != '' and ((len(team) > 5 and closestval <=3) or (len(team) <= 2 and closestval < 1) or (len(team) <= 5 and closestval <= 1))):
				daGame=teams[closests]
				if daGame['status'].count('PM ET') != 0 or daGame['status'].count('AM ET') != 0:
					if cancel:
						if origin in db['bets'] and closests in db['bets'][origin]:
							db['cash'][origin]=round(db['cash'][origin]+db['bets'][origin][closests][2],2)
							db['msgqueue'].append(['Your bet on '+db['bets'][origin][closests][0]+' has been canceled. Your wallet contains $'+cashVal(db['cash'][origin])+'.',msg_dest,msg_type])
							db['bets'][origin].pop(closests)
							sql.unique_set('data','bets',json.dumps(db['bets']))
							sql.unique_set('data','cash',json.dumps(db['cash']))
					else:
						if closest([params_orig,team.lower(),team.lower().replace('st','state')],[daGame['team1'].lower()]) < closest([params_orig,team.lower(),team.lower().replace('st','state')],[daGame['team2'].lower()]): daTeam='team1'
						else: daTeam='team2'
						if 'odds' in daGame and 'team1abbreviation' in daGame and 'team2abbreviation' in daGame:
							odds=daGame['odds'].split(' ')
							if odds.count('even') != 0:
								favored='team1'
								spread='0'
							else:
								favored=False
								spread=odds[1].replace('-','')
								if daGame['team1abbreviation']==odds[0]: favored='team1'
								elif daGame['team2abbreviation']==odds[0]: favored='team2'
							if favored:
								if not origin in db['bets']: db['bets'][origin]={}
								if closests in db['bets'][origin]:
									db['cash'][origin]=round(db['cash'][origin]+db['bets'][origin][closests][2],2)
									db['bets'][origin].pop(closests)
								if db['cash'][origin]-bet >= 0:
									db['cash'][origin]=round(db['cash'][origin]-bet,2)
									if favored == daTeam: 
										db['bets'][origin][closests]=[daGame[daTeam],'-'+spread,round(bet,2)]
									else: 
										db['bets'][origin][closests]=[daGame[daTeam],'+'+spread,round(bet,2)]
									sql.unique_set('data','bets',json.dumps(db['bets']))
									sql.unique_set('data','cash',json.dumps(db['cash']))
									db['msgqueue'].append(['Your bet that '+db['bets'][origin][closests][0]+' will cover the '+db['bets'][origin][closests][1]+' spread has been placed. Your wallet contains $'+cashVal(db['cash'][origin])+'.',msg_dest,msg_type])
								else: db['msgqueue'].append(['You have insufficient funds to place that bet. Your wallet contains $'+cashVal(db['cash'][origin])+'.',msg_dest,msg_type])
							else: db['msgqueue'].append(['Something went wrong: I couldn\'t figure out which team is favored. Please let harkatmuld know.',msg_dest,msg_type])
								
						else: 
							db['msgqueue'].append(['The spread for that game is not yet available.',msg_dest,msg_type])
							print daGame
				else: db['msgqueue'].append(['Bets must be placed before a game has begun. The current status of that game is: '+daGame['status']+'.',msg_dest,msg_type])
			elif bye==True:
				db['msgqueue'].append([closests+' has a bye week.',msg_dest,msg_type])
			else:
				db['msgqueue'].append(['Could not find a team or match.',msg_dest,msg_type])
	else:
		db['msgqueue'].append(['Invalid bet value. Value must be numerical.',msg_dest,msg_type])