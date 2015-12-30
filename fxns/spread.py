"""
Returns betting info by team name.
"!spread" can be replaced with "$" (i.e., "$UMiami" will produce the same result as "!spread UMiami")
"""
db['spread']=json.loads(sql.unique_get('data','spread'))
if len(' '.join(params)) != ' '.join(params).count('!'):
	def abbrev(words,abb,debug=False):
		con=abb
		for throw,ws in con.iteritems():
			#print words.lower()+'.'+ws[0].lower()+'.'
			if ws[0] != None and words.lower().strip()==ws[0].lower().strip(): words=ws[1]
			#if debug: print words+'.'+ws[0]+'.'+ws[1]+'.'
		return words
	if (origin.count('|') != 0 or origin.count('[') != 0) and ''.join(params).strip() == '':
		if origin.count('|') != 0: newo=origin[origin.find('|')+1:]
		elif origin.count('[') != 0: newo=origin[origin.find('[')+1:origin.find(']')]
		if newo.strip() != '': params=[newo]
	if ''.join(params).strip() != '':
		tbyname={}
		closestval=1000000
		closests=''
		teams=db['games_new']['fbs']
		params=abbrev(' '.join(params).lower(),db['abbreviations'])
		for a,b in teams.iteritems():
			if a != 'lastupdate':
				team1=b['team1'].lower().replace('(','').replace(')','')
				team2=b['team2'].lower().replace('(','').replace(')','')
				if params.count(' ') == 0: tclv=closest([params,params+' StateZ'],[team1,team2])
				else: tclv=closest([params,params.replace('st','state')],[team1,team2,team1+team2,team2+team1])
				if tclv < closestval:
					closestval=tclv
					closests=a
		if dest.lower()=='footballbot': msg_dest=origin
		else: msg_dest=dest

		user_pref=sql.get_user(origin)
		msg_type='PRIVMSG'
		if user_pref:
			if 'cmds' in user_pref and 'spread' in user_pref['cmds']:
				if user_pref['cmds']['spread']=='you': msg_dest=origin
				elif user_pref['cmds']['spread']=='channel' and dest.lower()!='footballbot': msg_dest=dest
			if 'pers_msgs' in user_pref and msg_dest==origin:
				if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
				elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'
		if closests != '' and closestval <= 2:
			tmtype='PRIVMSG'
			neutral=True
			nident=''
			if 'neutral' in db['games_new']['fbs'][closests]:
				neutral=db['games_new']['fbs'][closests]['neutral']
			if not neutral: nident='@ '
			if closests in db['games_new']['fbs'] and 'odds' in db['games_new']['fbs'][closests]:
				spdisp=db['games_new']['fbs'][closests]['odds']
				sptext=origin+': '+db['games_new']['fbs'][closests]['team1']+' '+nident+db['games_new']['fbs'][closests]['team2']+' - '+spdisp+chr(3)
				db['msgqueue'].append([sptext,msg_dest,msg_type,'score'])
		else: db['msgqueue'].append([origin+': Could not find a match for this week.',msg_dest,msg_type,None])
		#[msg,channel (all main chans), type(privmsg),identifier(None)]
