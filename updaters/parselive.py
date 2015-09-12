time.sleep(1)


###### SET VARIABLES FOR COMPATIBILITY WITH OLD DB
# CAN MOVE THIS TO PARSEDATA.PY WHEN YOU ELIMINATE THE LOADING OF DB.JSON
sql.cur.execute("""select * from data""")
a=sql.cur.fetchall()
db['language']={}
for b in a:
	if b[0]=='drunklevel' or b[0] =='drunksetting':
		if b[0] == 'drunklevel': db[b[0]]=int(b[1])
		else: db[b[0]]=b[1]
	elif b[0]=='msgqueue':
		db['msgqueue']=json.loads(b[1])
	else:
		if b[0].count('language') == 0: db[b[0]]=json.loads(b[1])
		else:
			db['language'][b[0][b[0].find('language-')+len('language-'):]]=json.loads(b[1])
db['msgqueue']=[]
#####################################

if time.time() > lloop+llen:
	#print 'loop'
	overallc+=1
	thedata=urlparse.parse_qs(urllib.urlopen('http://sports.espn.go.com/ncf/bottomline/scores?t'+str(int(time.time()))).read())
	ourgames=[]
	thedatastr=str(thedata)
	if len(thedatastr) > 50:
		if thedatastr.count('FINAL') == thedatastr.count('s_left'): overallc=10000
		for a,b in thedata.iteritems():
			if a[:10] == 'ncf_s_left':
				ourgames.append(a[10:])
		ourgames=list(OrderedDict.fromkeys(ourgames))
		gamedata={}
		for game in ourgames:
			#format: {"team1":team1,"team1score":team1score,"team2":team2,"team2score":team2score,'status':status}	
			#thedata['ncf_s_right'+game+'_count']]
			ourgame=thedata['ncf_s_left'+game][0]
			status=ourgame[::-1][1:ourgame[::-1].find('(')][::-1].strip()
			info=ourgame[::-1][ourgame[::-1].find('(')+1:][::-1].strip()
			while info.count('  ') != 0: info=info.replace('  ','---')
			info=info.replace(' at ','---')
			info=info.replace(' vs ','---')
			info=info.replace('@','---')
			info=info.replace('^','')
			info=info.split('---')
			t1rk=''
			t2rk=''
			info[1]=info[1].strip()
			if info[0][0] == '(': t1rk=info[0][1:info[0].find(')')]
			if info[1][0] == '(': t2rk=info[1][1:info[1].find(')')]
			#print info[1]
			team1=remove_rank(info[0]).strip()
			team2=remove_rank(info[1]).strip()
			if team1[::-1][0].isdigit() and team2[::-1][0].isdigit():
				team1name=team1[::-1][team1[::-1].find(' ')+1:][::-1]
				team1score=team1[::-1][:team1[::-1].find(' ')][::-1]
				team2name=team2[::-1][team2[::-1].find(' ')+1:][::-1]
				team2score=team2[::-1][:team2[::-1].find(' ')][::-1]
			else:
				team1name=team1
				team2name=team2
				team2score='0'
				team1score='0'
			gidentifier=team1name+team2name
			if 'ncf_s_url'+game in thedata:
				game_id=thedata['ncf_s_url'+game][0][thedata['ncf_s_url'+game][0].find('gameId=')+len('gameId='):].strip()
			else: game_id=''
			if game_id=='' and gidentifier in teamsold: game_id=teamsold[gidentifier]['gid']
			elif game_id=='': game_id=str(random.randrange(0,10000000))
			neutral=True
			if gidentifier in teamsold:	
				if 'neutral' in teamsold[gidentifier]: neutral=teamsold[gidentifier]['neutral']
			if gidentifier.count('San Jos') == 0 or gidentifier.count('St') == 0: gamedata[gidentifier]={"gid":game_id,"team1":team1name,"team1score":team1score,'neutral':neutral,"team2":team2name,"team2score":team2score,'status':status, 't1rk':t1rk,'t2rk':t2rk}
#			tw=json.dumps(gamedata)
			gamedata['lastupdate']=int(time.time())
		teams=gamedata
		#########
		####START MESSAGE ADDEDER HERE
		#json.dumps(db)
		if not 'lastcomm' in db: db['lastcomm']=[]
		if len(db['lastcomm']) > 10: db['lastcomm']=db['lastcomm'][1:]
		try:
			for gid,gddt in teams.iteritems():
				if gid != 'lastupdate':
					st=gddt['status'].strip()
					if gid in teamsold:
						if gddt != teamsold[gid]:
							#print gddt
							#print teamsold[gid]
							"""if gddt['status'].upper()=='0:00 IN 4TH' or gddt['status'].upper()=='0:00 4TH':
								st='FINAL'
								teams[gid]['status']=st
								gddt['status']=st
								db['games'][gid]['status']=st"""
							if gddt['status'].upper().count('FINAL')==1  or gddt['status'].upper().count('OT') == 1 or gddt['status'].upper().count('15:00') != 0 or gddt['status'].upper().count('HALFTIME') != 0 or gddt['team1score'] != teamsold[gid]['team1score']	or gddt['team2score'] != teamsold[gid]['team2score']:		
								#print gddt
								#print teamsold[gid]
								commentary=''			
								st=gddt['status'].strip()
								st=st.replace('15:00','BEGIN').replace(' IN ',' ')
								#[msg,channel (all main chans), type(privmsg),identifier(None)]
								t1name=gddt['team1']
								t2name=gddt['team2']
								shorts=artolower(db['shorten'])
								if t1name.lower() in shorts and shorts[t1name.lower()].strip() != '': t1name=shorts[t1name.lower()]
								if t2name.lower() in shorts and shorts[t2name.lower()].strip() != '': t2name=shorts[t2name.lower()]
								t1=t1name
								t2=t2name
								cis=artolower(json.loads(sql.unique_get('data','colors')))
								t1rk=''
								t2rk=''
								#if gddt['t1rk'] != '': t1rk='('+gddt['t1rk']+') '
								#if gddt['t2rk'] != '': t2rk='('+gddt['t2rk']+') '
								rks=artolower(db['ranks'])
								if gddt['team1'].lower() in rks and rks[gddt['team1'].lower()] != None: t1rk='('+rks[gddt['team1'].lower()]+') '
								if gddt['team2'].lower() in rks and rks[gddt['team2'].lower()] != None: t2rk='('+rks[gddt['team2'].lower()]+') '
								t1=t1rk+t1+' '+gddt['team1score']
								t2=t2rk+t2+' '+gddt['team2score']
								ntwkadd=''
								comm2=''
								poss=''
								if gddt['team2score'] > teamsold[gid]['team2score'] or gddt['team1score'] > teamsold[gid]['team1score']:
									mrcur=most_recent_play(gddt['gid'])
									comm2=mrcur[0]
									poss=mrcur[1]
								if poss.lower() == t1name.lower(): t1=t1+' (:)'
								elif poss.lower() == t2name.lower(): t2=t2+' (:)'
								if gddt['team1'].lower() in cis: t1=chr(3)+str(cis[gddt['team1'].lower()][0])+','+str(cis[gddt['team1'].lower()][1])+t1.strip()+chr(3)
								if gddt['team2'].lower() in cis: t2=chr(3)+str(cis[gddt['team2'].lower()][0])+','+str(cis[gddt['team2'].lower()][1])+t2.strip()+chr(3)
								if st.count('BEGIN') == 1 and st.count('1ST') == 1 and gid in db['ntwks']:
									ntwkadd=' - '+db['ntwks'][gid]
								if db['lastcomm'].count(t1+t2+comm2) == 0 and comm2 != '': db['lastcomm'].append(t1+t2+comm2)
								elif db['lastcomm'].count(t1+t2+comm2) != 0: comm2=''
								if comm2 == '':
									datm=''
									datmn=''
									if gddt['team2score'] != teamsold[gid]['team2score']:
										datm=gddt['team2']
										datmn='team2'
									elif gddt['team1score'] != teamsold[gid]['team1score']:
										datm=gddt['team1']
										datmn='team1'
									if datm != '':
										dacomm=''
										if gddt[datmn+'score'] == int(teamsold[gid][datmn+'score'])+6: dacomm=datm+' TOUCHDOWN!'
										if gddt[datmn+'score'] == int(teamsold[gid][datmn+'score'])+3: dacomm=datm+' FIELD GOAL!'
										if gddt[datmn+'score'] == int(teamsold[gid][datmn+'score'])+1: dacomm=datm+' EXTRA POINT GOOD!'
										if dacomm != '': comm2=dacomm
								stats_to_append=''
								if st.count('FINAL') == 1:
									sts=stats(gddt['gid'])
									stats_to_append=' -- GAME STATS: '+sts+chr(3)
								if comm2.strip() != '': comm2=' '+comm2
								if gddt['neutral'] == True: cnctr='-'
								else: cnctr=' @ '
								msg='\x02'+t1+' '+cnctr+' '+t2+'\x02'+comm2+' ('+st+ntwkadd+')'+stats_to_append
								if not msg in yamsg:
									db['msgqueue'].append([msg,None,None,'score'])
									yamsg.append(msg)
									#print 'doing it'
		except:
			print "ERROR!"
			open('/home/fbbot/cfb/logs/error.log','a').write(str(traceback.format_exc())+str(gddt)+str(gid)+'\r\n')
			teamsold=teams
		newdb=db
		sql.unique_set('data','games',json.dumps(teams))
		sql.unique_set('data','msgqueue',json.dumps(db['msgqueue']))
		db['games']={}
		for addmsg in newdb['msgqueue']:
			if not addmsg in db['msgqueue']: db['msgqueue'].append(addmsg)
		#db['msgqueue']=[]
		#print db
		tw=json.dumps(db)
		tw=tw.encode('ascii','ignore')
		teamsold=teams
			###################
		####EDND MESSAGE ADDER
		####################
		####################
		#print json.dumps(gamedata)
		if json.dumps(gamedata).count('team1score') == json.dumps(gamedata).count('PM ET')+json.dumps(gamedata).count('AM ET') or json.dumps(gamedata).count('team1score') == json.dumps(gamedata).count('DELAYED')+json.dumps(gamedata).count('PM ET')+json.dumps(gamedata).count('AM ET')+json.dumps(gamedata).count('FINAL'):
			overallc=10000
	else: overallc=10000
	lloop=time.time()
	llen=random.randrange(8,12)
