"""
Returns my current blood alcohol level
"""
if dest.lower()=='footballbot': msg_dest=origin
else: msg_dest=dest

user_pref=sql.get_user(origin)
msg_type='PRIVMSG'
if user_pref:
	if 'cmds' in user_pref and 'alcohol' in user_pref['cmds']:
		if user_pref['cmds']['alcohol']=='you': msg_dest=origin
		elif user_pref['cmds']['alcohol']=='channel' and dest.lower()!='footballbot': msg_dest=dest
	if 'pers_msgs' in user_pref and msg_dest==origin:
		if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
		elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'
db['msgqueue'].append(['My current circuit alcohol level is '+str(round(dlevel/100,2))+'%.',msg_dest,msg_type])