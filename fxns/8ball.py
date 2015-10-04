if dest.lower()=='footballbot': msg_dest=origin
else: msg_dest=dest
msg_type='PRIVMSG'
user_pref=sql.get_user(origin)
if user_pref:
	if 'cmds' in user_pref and '8ball' in user_pref['cmds']:
		if user_pref['cmds']['8ball']=='you': msg_dest=origin
		elif user_pref['cmds']['8ball']=='channel' and dest.lower()!='footballbot': msg_dest=dest
	if 'pers_msgs' in user_pref and msg_dest==origin:
		if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
		elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'
par=' '.join(params).lower()
if len(par) < 10 and par.count('is') == 0 and par.count('?') == 0 and par.count('will') == 0 and par.count('should') == 0 and par.count('could') == 0 and par.count('do') == 0 and par.count('has') == 0 and par.count('does') == 0 and par.count('when') == 0 and par.count('why') == 0 and par.count('who') == 0:  db['msgqueue'].append([origin+': That\'s not a question!',dest])
else:
	if par.count(' or ') == 1:
		opt1=par[par.find(' or ')+4:].strip()
		if opt1.count(' ') != 0: opt1=opt1[:opt1.find(' ')].strip()
		opt2=par[::-1]
		opt2=opt2[opt2.find(' ro ')+4:].strip()
		if opt2.count(' ') != 0: opt2=opt2[:opt2.find(' ')].strip()
		opt1=opt1.replace('?','')
		opt2=opt2.replace('?','')
		opt2=opt2[::-1]
		db['msgqueue'].append([origin+': '+random.choice(db['language']['verbs'])+'ing '+random.choice([opt1,opt2]),msg_dest])
	else: db['msgqueue'].append([origin+': '+random.choice(db['language']['eightball']),msg_dest,msg_type])