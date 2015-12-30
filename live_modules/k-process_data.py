
tlana=''
just_authed=[]
#print commands_pending_auth
for line in lines:
	isText=False
	tlana=' '.join(line)
	#print line
	#CHECK FOR NICKSERV PING REPLY###
	#:nickserv!nickserv@services. notice footballbot :harkatmuld acc 1
	
	if ((tlana.lower().count('footballbot') != 0 or tlana.count('harkat') != 0 or tlana.count(' bot ') != 0)) and tlana.count('freenode.net') == 0 and tlana.count('PING') == 0 and prefix=='':
		user=line[0][1:line[0].find('!')]
		if user.lower() != 'footballbot' and user.lower() != 'harkatmuld': db['msgqueue'].append([tlana,'harkatmuld',None,None,False])
	if line[1] == '353':
		if time.time()-last_users_update > 30: 
			#print time.time()-last_users_update
			new_users_online=[]
			mods_list=[]
		users_raw=tlana[1:]
		users_raw=users_raw[users_raw.find(':')+1:]
		users=users_raw.split(' ')
		for user in users:
			if user[0]=='@' or user[0]=='+': 
				if user[0]=='@' and not user in mods_list: mods_list.append(user)
				user=user[1:]
			if not user in new_users_online: new_users_online.append(user)
		last_users_update=time.time()
	if line[1] == '366' and line[3] != '#redditcfb':
		users_online=new_users_online
	if line[0].lower()=="ping":
		s.send("PONG %s\r\n" % line[1])
		#print "PONG %s\r\n" % line[1]
		#open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': PING PONG\r\n')
	elif line[1].lower() == 'join':
		user=line[0][1:line[0].find('!')]
		client=line[0][line[0].find('!'):]
		client=client[:client.find(' ')].lower()
		channel_join=line[-1].strip()
		if channel_join=='#redditcfb': users_in_channel.append(user)
		user_pref=sql.get_user(user)
		if user_pref and 'most_recent_msgs' in user_pref and user_pref['most_recent_msgs']=='Yes':
			print user_pref
			last_msgs_to_send=[]
			if channel_join.replace('#','').lower() in last_msgs:
				for msg in last_msgs[channel_join.replace('#','').lower()]:
					if time.time()-msg[1] < 60*15:
						last_msgs_to_send.append(msg)
			if len(last_msgs_to_send) != 0:
				db['msgqueue'].append(['Most recent messages sent to '+channel_join+':',user])
				for msg in last_msgs_to_send:
					time_ago=time.time()-msg[1]
					if time_ago > 60: time_ago=str(int(time_ago/60))+'m ago'
					else: time_ago=str(int(time_ago))+'s ago'
					msg_type='PRIVMSG'
					db['msgqueue'].append(['\x02'+time_ago+'\x02 '+msg[0],user,msg_type,None,False])
	elif line[1].lower() == 'part' or line[1].lower() == 'quit':
		user=line[0][1:line[0].find('!')]
		channel_part=line[-2].strip()
		while user in users_in_channel:
			users_in_channel.remove(user)
	elif line[1]=='NICK':
		user=line[0][1:line[0].find('!')]
		newnick=line[2][1:]
		sql.cur.execute("""select username from me;""" )
		a=sql.cur.fetchall()
		list_of_users=[]
		for usern in a: #user[0] = username, [1] = following
			list_of_users.append(usern[0])
		if user in list_of_users:
			sql.cur.execute("""update me set username='"""+MySQLdb.escape_string(newnick)+"""' where username='"""+MySQLdb.escape_string(user)+"""' limit 1;""")
			#print """update me set username='"""+MySQLdb.escape_string(newnick)+"""' where username='"""+MySQLdb.escape_string(user)+"""' limit 1;"""
	elif len(line) >3: #[':NickServ!NickServ@services.', 'NOTICE', 'FootballBot', ':harkatmuld', 'ACC', '3']
		if line[0]==':NickServ!NickServ@services.' and line[1] == 'NOTICE' and line[4]=='ACC':
			if line[5] == '3':
				just_authed.append(line[3][1:])
				if line[3][1:] in commands_pending_auth:
					for line_pending in commands_pending_auth[line[3][1:]]:
						lines.append(line_pending)
			elif line[5] == '0': #not registered
				db['msgqueue'].append(['To use this command, you must register your nickname with freenode and log in. To register, type "/ns REGISTER <password> <email-address>".',line[3][1:]])
			elif line[5] == '1' or line[5] == '2': #not authed			
				db['msgqueue'].append(['To use this command, you must authenticate to freenode. To log in, type "/ns identify <password>".',line[3][1:]])
			commands_pending_auth.pop(line[3][1:])
		user=line[0][1:line[0].find('!')]
		origin=user
		dest=line[2]
		if dest.count('#') != 0 and line[1]=='PRIVMSG':
			if not dest.replace('#','').lower() in last_msgs: last_msgs[dest.replace('#','').lower()]=[]
			last_msgs[dest.replace('#','').lower()].append(['<'+origin+'> '+' '.join(line[3:])[1:],time.time()])
			for chan in last_msgs:
				if len(last_msgs[chan]) > 5:
					last_msgs[chan].pop(0)
		######NORMAL STUFF
		if not origin in user_messages: user_messages[origin]=[]
		if dest=='#redditcfb': user_messages[origin].append(time.time())			
		if not user in users_in_channel and dest=='#redditcfb': users_in_channel.append(user)

		open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M:%S')+': '+user+' to '+line[2]+': '+' '.join(line[3:])[1:]+'\r\n')
		#open('logs/interactw.log','a').write(time.strftime('%a %b %d %H:%M')+': '+user+' to '+line[2]+': '+' '.join(line[3:])[1:]+'\r\n')
		######################-TWITTER STATUS DISPLAY-####################
		turl=''
		if ' '.join(line).lower().count('reddit.com/') == 1 and ' '.join(line).lower().count('/comments/') != 0:
			dest=line[2]
			tl=' '.join(line)
			turl='http://www.'+tl[tl.find('reddit.com/'):]
			if turl.count(' ') != 0: turl=turl[:turl.find(' ')]
			if turl[-1] == '/': turl=turl[:-1]
			if len(turl[::-1][:turl[::-1].find('/')]) < 15:
				r = praw.Reddit('<USERAGENT>')
				comment = r.get_submission(turl).comments[0]
				if dest == 'footballbot': dest=user
				#print comment.author
				db['msgqueue'].append([str(comment.author)+': '+comment.body[:400]+chr(3),dest,None,None,False])
		if ' '.join(line).count('twitter.com/') == 1 and (' '.join(line).count('/status/') == 1 or ' '.join(line).count('/statuses/') == 1) and (line[2]!='#redditcfb' and line[2] != '#cfbot'):
			for a in line:
				if a.count('twitter.com') == 1:
					ts=''
					turl=a
					if a.count('statuses') == 1: ts='statuses'
					elif a.count('status') == 1: ts='status'
					#print ts
					#print a
					tid=a[a.find(ts)+len(ts)+1:]
					#if tid.count('/') != '': tid=tid[:tid.find('/')]
			dest=line[2]
			CONSUMER_KEY = ""
			CONSUMER_SECRET = ""
			ACCESS_KEY = ""
			ACCESS_SECRET = ""
			consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
			access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
			client = oauth.Client(consumer, access_token)
			#print tid
			timeline_endpoint = "https://api.twitter.com/1.1/statuses/show.json?id="+tid
			resp = client.request(timeline_endpoint)
			#print resp
			response=resp[0]
			data=resp[1]
			#print response
			tweets = json.loads(data)
			#print tweets
			#print tweets
			#print tid
			tweets['text']=tweets['text'].encode('ascii','ignore')
			tweets['text']=(u''+tweets['text']).decode('utf8')
			txt=tweets['text'].replace('pic.twitter.com','https://pic.twitter.com')
			repto=''
			if 'in_reply_to_screen_name' in tweets:
				if tweets['in_reply_to_screen_name'] != None and len(tweets['in_reply_to_screen_name']) > 1: repto=(u''+tweets['in_reply_to_screen_name']).decode('utf8')
			twiuser=turl[turl.find('twitter.com/')+len('twitter.com/'):]
			twiuser=twiuser[:twiuser.find('/')]
			if repto != '': repto=', replying to '+repto
			db['msgqueue'].append(['@'+twiuser+repto+': '+txt+chr(3),dest,None,None,False])
		##############
		ful=' '.join(line)
		if len(line[3]) > 2:
			##### INTERPRET PLAIN LANGUAGE MESSAGES
		
			cur_l=' '.join(line[3:])
			msg_type_p='PRIVMSG'
			if dest.lower() != 'footballbot': msg_dest_p=dest
			else: msg_dest_p=origin
			if (keywords(cur_l, ['bot ',' rank']) or keywords(cur_l, ['bot ',' poll'])) and not keywords(tlana,['github']) and not keywords(tlana,['solbot']):
				db['msgqueue'].append([origin+': I get my rankings from the /r/cfb poll, available at http://rcfbpoll.com/. Rankings beyond 25 are based on the number of votes each team receives.',msg_dest_p,'PRIVMSG'])
			elif keywords(cur_l,['what','is','score']) or keywords(cur_l,['what','was','score']) or keywords(cur_l,['what','are','score']) or keywords(cur_l,["what'",'score']) or keywords(cur_l,["whats",'score']) or keywords(cur_l,["when'",'game']) or keywords(cur_l,['when','is','game']) or keywords(cur_l,['when','are','game']) or keywords(cur_l,["when'",'playing']) or keywords(cur_l,['when','is','playing']) or keywords(cur_l,['when','are','playing']) or keywords(cur_l,['what','channel']) or keywords(cur_l,['what','network']) or keywords(cur_l,['what','time']) or keywords(cur_l,['what','time','playing']):
				cur_l_orig=cur_l
				cur_l=re.split('and|,|/',cur_l)
				games=[]
				#print cur_l
				for game in cur_l:
					gm_text=remove_text(game,['when','playing','channel',' on','whats',"what's",'what','scores','games','score','game',' was ', ' and ',' for ',' the ',' is ',' are ','.','?','!',':',"'s",'time','>','gonna','start',' hell','network','its','it','at','kick','off','play','also','does']).strip()
					if gm_text != '' and gm_text.count(' ') <= 3 and cur_l_orig.count(' ') < 10: games.append(gm_text)
				print games
				for game in games:
					if game.count(' vs') != 0: game=game[:game.find(' vs')]
					if game.count(' ') != 0 and game.count(' st') == 0: game=game[:game.find(' ')] #a lot of people, when asking what a score is or a channel is, seem to use both teams. so hopefully this will help without message up too much.
					games_nextloop.append(game)
					if not 'score'+'_ucmd' in cached: cached['score_ucmd']=open('/home/fbbot/cfb/fxns/score.py').read()
					params=[game]
					db['msgqueue'].append(['did it','harkatmuld'])
					isText=True
					type_of_text=''
					if keywords(cur_l_orig,["when'",'game']) or keywords(cur_l_orig,['when','is','game']) or keywords(cur_l_orig,['when','are','game']) or keywords(cur_l_orig,["when'",'playing']) or keywords(cur_l_orig,['when','is','playing']) or keywords(cur_l_orig,['when','are','playing']) or keywords(cur_l_orig,['what','time','game']) or keywords(cur_l_orig,['what','time','playing']):
						type_of_text='time'
					elif keywords(cur_l_orig,['what','channel']) or keywords(cur_l_orig,['what','network']):
						type_of_text='channel'
					isAutoDetect=True
					exec cached['score_ucmd']		
				isAutoDetect=False
			
			
			#### INTERPRET COMMANDS
			
			if line[3][1] == '$' and line[3][2].isalpha(): line[3]=':!$'+line[3][2:]
			elif line[3][1] == '?' and line[3][2].isalpha():
				line=line[:3]+[':!info']+line[3:]
				if len(line) >= 4: line[4]=line[4][2:]
			elif line[3][1] == '%':
				line=line[:3]+[':!player']+line[3:]
				if len(line) >= 4: line[4]=line[4][2:]
			allowit=True
			if user in pastcmd:
				if len(pastcmd[user]) > 15 and user.lower().count('dublock') == 0 and user.lower().count('harkat') == 0: allowit=False
			if ' '.join(line[3:]).count('!') == len(' '.join(line[3:]))-1: allowit=False
			#print  ' '.join(line[3:]).count('!')
			#print len(' '.join(line[3:]))
			if line[3][1]=='!' and allowit:
				#print line
				#if user.lower().count('ptyyy') != 0: dlevel=1000000
				if not user in pastcmd: pastcmd[user]=[]
				pastcmd[user].append(time.time())
				if not 'fxnsdir' in cached:
					os.system('ls -lah /home/fbbot/cfb/fxns/ > .fxnsdir')
					cached['fxnsdir']=open('.fxnsdir').read()
					os.system('rm .fxnsdir')
				if cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py\n') == 0 and cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py ') == 0:
					line[3]=line[3][2:].lower()
					#db['msgqueue'].append([line[3][0],'harkatmuld'])
					if line[3][0] == '$':
						line=line[:3]+[':!spread']+line[3:]
						line[4]=line[4][1:]
					elif line[3][0] == '#':
						line=line[:3]+[':!twi']+line[3:]
						line[4]=line[4][1:]
					elif line[3][0] == '*':
						line=line[:3]+[':!player']+line[3:]
						line[4]=line[4][1:]
					elif line[3][0] == '?': line=line[:3]+[':!info']+line[3:]
					else: line=line[:3]+[':!score']+line[3:]
					#print line
				if (' '.join(line[3:]).count('.') ==0 or ' '.join(line[3:]).count('!player ') != 0 or ' '.join(line[3:]).count('!bet ') != 0) and ((cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py\n') != 0) or (cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py ') != 0)):
					user=line[0][1:line[0].find('!')]
					dest=line[2].lower()
					params=line[4:]
					params=' '.join(params).lower()
					params=params.replace('\n','').replace('\r','')
					params=params[:300]
					if len(params.strip()) == 0: params=[]
					else: params=params.split(' ')
					if not line[3][2:].lower()+'_ucmd' in cached: cached[line[3][2:].lower()+'_ucmd']=open('/home/fbbot/cfb/fxns/'+line[3][2:].lower()+'.py').read()
					exec cached[line[3][2:].lower()+'_ucmd']
