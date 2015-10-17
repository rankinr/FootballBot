exec(open('/home/fbbot/cfb/common_functions.py')) #load custom functions
l_users_in_channel=lsttolower(users_online)
#print l_users_in_channel
for update,users in db['play_updates'].iteritems():
	for user in users:
		if user.lower() in l_users_in_channel:
			msg_dest=user
			user_pref=sql.get_user(user)
			msg_type='PRIVMSG'
			if user_pref:
				if 'pers_msgs' in user_pref:
					if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
					elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'
			db['msgqueue'].append([gameInfo(update,True,True)+'* *'+oinfo,msg_dest,msg_type,'score'])
sql.unique_set('data','play_updates','{}')