while len(db['msgqueue']) != 0:
	sql.unique_set('data','drunklevel',str(int(db['drunklevel'])+1))
	#[msg,channel (all main db['config']['chans']), type(privmsg),identifier(None)]
	#print db['msgqueue']
	#print db['msgqueue'][0][0]
	db['msgqueue'][0][0]=db['msgqueue'][0][0].replace(u'\xe9','e').replace(u'\xb7','').decode('utf8').replace('\r','').replace('\n','')
	if len(db['msgqueue'][0]) >=5: cursing=db['msgqueue'][0][4]
	else: cursing=True
	if len(db['msgqueue'][0])  >= 4: 
		midentifier=db['msgqueue'][0][3]
	else: midentifier=None
	if len(db['msgqueue'][0]) >=3:
		if db['msgqueue'][0][2] == None: mtype='PRIVMSG'
		else: mtype=db['msgqueue'][0][2]
	else: mtype='PRIVMSG'
	if len(db['msgqueue'][0]) >=2:
		if db['msgqueue'][0][1]==None: mchannel=db['config']['chans']
		else: mchannel=db['msgqueue'][0][1]
	else: mchannel=db['config']['chans']
	msg=db['msgqueue'][0][0][:550].replace('&nbsp;',' ')
	abob=''
	msg=msg.strip().replace('%ABOB%',abob)
	if abob != '': msg+=chr(3)
	#msg, mchannel, mtype, midentifier
	if (lastmsg != msg or time.time() > lastsent+3 or 1==1) and msg != '':
		if isinstance(mchannel,basestring): mchannel={'all':[mchannel]}
		elif isinstance(mchannel,list): mchannel={'all':mchannel}
		if midentifier != None:
			if midentifier in mchannel:
				if mchannel != None:
					if mchannel[midentifier] != None: sendto=mchannel[midentifier]
			else:
				if 'all' in mchannel: sendto=mchannel['all']
				else: sendto=[]
		else:
			if 'all' in mchannel:
				sendto=mchannel['all']
			else: sendto=[]
		if 'all' in mchannel:
			for a in mchannel['all']:
				if sendto.count(a) == 0: sendto.append(a)
		#print '4'
		for chan in sendto:
			#print '5'
			if chan == '#redditcfb' and len(rcfb_msgs) > 30:
				for msg_time in rcfb_msgs:
					if time.time()-msg_time > 9:
						rcfb_msgs.pop(rcfb_msgs.index(msg_time))
			if chan != '#redditcfb' or len(rcfb_msgs) < 40 or 1==1:
				if chan == '#redditcfb': rcfb_msgs.append(time.time())
				colordi=''
				if cursing and chan.lower() != 'nickserv' and midentifier != 'comment' and midentifier != 'comments':
					if msg.count('My current circuit alcohol level is') == 1: dlevel=dlevel*2
					"""
					#drunksettings ->
						curse
						names
						appendages
						toodrunk
						duplicate
						slur
						insert
						SUBS:
							randomize
							min
				"""
					if random.randrange(0,db['drunksettings']['curse']['randomize']) < dlevel and msg.count(' ') > 2 and dlevel > db['drunksettings']['curse']['min']:
						pt=random.randrange(0,len(msg)-1)
						loopcmsg=0
						while msg[pt] != ' ' and msg[pt] and loopcmsg < 10:
							pt=random.randrange(0,len(msg)-1)
							loopcmsg+=1
						curse=random.choice(db['language']['curses'])
						msg=msg[:pt]+' '+curse.upper()+' '+msg[pt+1:]
					namecalled=False
					if random.randrange(0,db['drunksettings']['names']['randomize']) < dlevel and dlevel > db['drunksettings']['names']['min']:
						addition=random.choice(db['language']['names']).upper()
						if msg[-1] == '.': msg=msg[:-1]
						plu=''
						if midentifier=='score': plu='S'	
						rannum=random.randrange(0,5)	
						if rannum == 2: msg=addition+plu+', here\'s what\'s up. '+msg+'!'*random.randrange(1,15) 
						elif rannum==3 or rannum==4: addition+plu+', '+msg
						else: msg=msg+' you '+addition+plu+'!'*random.randrange(1,15)
						namecalled=True
					if not namecalled and random.randrange(0,db['drunksettings']['appendages']['randomize']) < dlevel and dlevel > db['drunksettings']['appendages']['min']:
						appendage=random.choice(db['language']['appendages']).strip()
						if appendage[-1]=='-': msg=appendage[:-1]+' '+msg
						elif appendage[0]=='-': msg=msg+' '+appendage[1:]
						else: msg=random.choice([msg+' '+appendage+'!'*random.randrange(1,10),appendage+'!'*random.randrange(0,3)+' '+msg])
					if random.randrange(0,db['drunksettings']['toodrunk']['randomize']) < dlevel and dlevel >= db['drunksettings']['toodrunk']['min']:
						msg+=random.choice(db['language']['toodrunk'])
					cedit=0
					while cedit <=10:
						cedit+=1
						if len(msg) > 3 and random.randrange(0,db['drunksettings']['duplicate']['randomize']) < dlevel and dlevel > db['drunksettings']['duplicate']['min']:
							pt=random.randrange(0,len(msg)-1)
							if count_numbers(msg[pt]) == 0 and msg[pt] != ',' and (msg[:pt].count('*') == 0 or msg[pt:].count('*') == 0): msg=msg[:pt]+msg[pt]+msg[pt:]
					if random.randrange(0,db['drunksettings']['slur']['randomize']) < dlevel and msg.strip().count(' ') != 0 and dlevel > db['drunksettings']['slur']['min']:
						strep=0
						enrep=0
						loopcspc=0
						while (msg[strep:]+msg[:enrep]).count(' ') == 0 and loopcspc < 500:
							loopcspc+=1
							strep=random.randrange(0,len(msg))
							enrep=strep+random.randrange(0,3)
						if count_numbers(msg[strep:enrep]) == 0 and (msg[:strep].count('*') == 0 or msg[enrep:].count('*') == 0): msg=msg[:strep]+msg[enrep:]
					cedit=1
					while cedit <= 4:
						cedit+=3
						if random.randrange(0,db['drunksettings']['insert']['randomize']) < dlevel and dlevel > db['drunksettings']['insert']['min']:
							randadd=''
							randlen=random.randrange(1,3)
							while len(randadd) < randlen:
								randadd+=random.choice(['a','e','i','o','u'])
							strep=random.randrange(0,len(msg))
							enrep=strep+random.randrange(0,3)
							if count_numbers(msg[strep:enrep]) == 0 and (msg[:strep].count('*') == 0 or msg[:enrep].count('*') == 0): msg=msg[:strep]+randadd+msg[enrep:]
		#		if msg.count(chr(3)) == 0 and chan.lower() != 'nickserv': colordi=chr(3)+'0,1'	
				h=HTMLParser()
	#			msg='test'
				db['msgqueue'].pop(0)
				sql.unique_set('data','msgqueue',json.dumps(db['msgqueue']))
				s.send(mtype+" "+chan+" :"+colordi+h.unescape(msg.replace('*','').decode('utf8'))+"\r\n")
				#print mtype+" "+chan+" :"+colordi+msg.encode('ascii','ignore')
				open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': sent to '+chan+": "+colordi+msg+"\r\n")
				#open('logs/interactw.log','a').write(time.strftime('%a %b %d %H:%M')+': sent to '+chan+": "+colordi+msg+"\r\n")
	else:
		if msg == '': db['msgqueue'].pop(0)
		else: print '?'
	lastsent=time.time()
	lastmsg=msg