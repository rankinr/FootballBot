for line in lines:
	tlana=' '.join(line)
	#CHECK FOR NICKSERV PING REPLY###
	
	#:nickserv!nickserv@services. notice footballbot :harkatmuld acc 1
	if ((tlana.lower().count('footballbot') != 0 or tlana.count('harkat') != 0 or tlana.count(' bot ') != 0)) and tlana.count('freenode.net') == 0 and tlana.count('PING') == 0:
		user=line[0][1:line[0].find('!')]
		if user.lower() != 'footballbot' and user.lower() != 'harkatmuld': db['msgqueue'].append([tlana,'harkatmuld',None,None,False])
	if line[0].lower()=="ping":
		s.send("PONG %s\r\n" % line[1])
		#print "PONG %s\r\n" % line[1]
		#open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': PING PONG\r\n')
	elif line[1].lower() == 'join':
		user=line[0][1:line[0].find('!')]
		channel_join=line[-1].strip()
		if channel_join=='#redditcfb': users_in_channel.append(user)
	elif line[1].lower() == 'part' or line[1].lower() == 'quit':
		user=line[0][1:line[0].find('!')]
		channel_part=line[-2].strip()
		while user in users_in_channel:
			users_in_channel.remove(user)
	elif len(line) >3:
		user=line[0][1:line[0].find('!')]
		origin=user
		dest=line[2]
		if not origin in user_messages: user_messages[origin]=[]
		if dest=='#redditcfb': user_messages[origin].append(time.time())			
		if not user in users_in_channel and dest=='#redditcfb': users_in_channel.append(user)

		open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': '+user+' to '+line[2]+': '+' '.join(line[3:])[1:]+'\r\n')
		open('logs/interactw.log','a').write(time.strftime('%a %b %d %H:%M')+': '+user+' to '+line[2]+': '+' '.join(line[3:])[1:]+'\r\n')
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
		if ' '.join(line).count('twitter.com/') == 1 and (' '.join(line).count('/status/') == 1 or ' '.join(line).count('/statuses/') == 1) and (line[2]!='#redditcfb'):
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
			if line[3][1] == '$' and line[3][2].isalpha(): line[3]=':!$'+line[3][2:]
			elif line[3][1] == '?' and line[3][2].isalpha():
				line=line[:3]+[':!info']+line[3:]
				if len(line) >= 4: line[4]=line[4][2:]
			elif line[3][1] == '*':
				line=line[:3]+[':!player']+line[3:]
				if len(line) >= 4: line[4]=line[4][2:]
			allowit=True
			if user in pastcmd:
				if len(pastcmd[user]) > 4 and user.lower().count('dublock') == 0 and user.lower().count('harkat') == 0: allowit=False
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
				if (' '.join(line[3:]).count('.') ==0 or ' '.join(line[3:]).count('!player ') != 0) and ((cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py\n') != 0) or (cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py ') != 0)):
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