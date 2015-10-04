"""
Returns stats for game.
"""
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
		if 'cmds' in user_pref and 'stats' in user_pref['cmds']:
			if user_pref['cmds']['stats']=='you': msg_dest=origin
			elif user_pref['cmds']['stats']=='channel' and dest.lower()!='footballbot': msg_dest=dest
		if 'pers_msgs' in user_pref and msg_dest==origin:
			if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
			elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'
	if closests != '' and closestval <= 2:
		ourgame=teams[closests]
		cis=artolower(db['colors'])
		if ourgame['team1'].lower() in cis: t1=chr(3)+str(cis[ourgame['team1'].lower()][0])+','+str(cis[ourgame['team1'].lower()][1])+ourgame['team1']
		else: t1=ourgame['team1']
		if ourgame['team2'].lower() in cis: t2=chr(3)+str(cis[ourgame['team2'].lower()][0])+','+str(cis[ourgame['team2'].lower()][1])+ourgame['team2']
		else: t2=ourgame['team2']
		t1=t1+' '+ourgame['team1score']
		t2=t2+' '+ourgame['team2score']
		if t1.count(chr(3)) != 0: t1+=chr(3)
		if t2.count(chr(3)) != 0: t2+=chr(3)
		tmtype='PRIVMSG'
		stsm=splitMessage(stats(ourgame['gid']))
		for sts in stsm:
			db['msgqueue'].append([origin+': '+t1+'-'+t2+' '+sts,msg_dest,msg_type,'score'])
	else: db['msgqueue'].append([origin+': Could not find a match for this week...',msg_dest,msg_type,None])
	#[msg,channel (all main chans), type(privmsg),identifier(None)]
