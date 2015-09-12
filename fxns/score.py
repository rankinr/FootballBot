"""Looks up games by team name ("!score UMiami"), conference ("!score ACC") or time ("!score 330").
"score" can be omitted (i.e., "!UMiami", "!ACC", or "!330" will produce the same results as above)
""" 


un_team=False
newo=''


if (origin.count('|') != 0 or origin.count('[') != 0):
	if origin.count('|') != 0: newo=origin[origin.find('|')+1:]
	elif origin.count('[') != 0: 
		newo=origin[origin.find('[')+1:]
		if newo.count(']') != 0: newo=newo[:newo.find(']')]
	if  ''.join(params).strip() == '' and newo.strip() != '': params=[newo.strip()]
	if newo.strip() != '': un_team=match(newo)

	
if ''.join(params).strip() != '':
	tbyname={}
	closestval=1000000
	closests=''
	teams=db['games']
	params=abbrev(' '.join(params).lower(),db['abbreviations'])
	for a,b in teams.iteritems():
		if a != 'lastupdate':
			team1=b['team1'].lower().replace('(','').replace(')','')
			team2=b['team2'].lower().replace('(','').replace(')','')
			if params.count(' ') == 0: tclv=closest([params.lower(),params.lower()+' StateZ',params.lower().replace('st','state')],[team1.lower(),team2.lower()])
			else: tclv=closest([params.lower(),params.lower().replace('st','state')],[team1.lower(),team2.lower(),team1.lower()+team2.lower(),team2.lower()+team1.lower()])
			if tclv < closestval:
				closestval=tclv
				closests=a
	if dest=='footballbot' or dest=='footballtestbot': dest=origin

	if closests != '' and closestval <= 3:
		db['msgqueue'].append([gameInfo(closests,True,True)+'* '+shorten_url('http://sports.espn.go.com/ncf/boxscore?gameId='+teams[closests]['gid'])+'*',dest,tmtype,'score'])
	else:
		conf=[]
		closest_conf=''
		closest_conf_val=100000
		db['conferences']=json.loads(sql.unique_get('data','conferences'))
		for a,b in db['conferences'].iteritems():
			clv_conf=closest([params.lower()],[a.lower()])
			if clv_conf  < closest_conf_val:
				closest_conf_val=clv_conf
				closest_conf=a
		#db['msgqueue'].append([closest_conf+str(closest_conf_val),'harkatmuld','PRIVMSG'])
		if closest_conf != '' and closest_conf_val <= 3:
			#closest_conf_val
			for c in db['conferences'][closest_conf]:
				for a,b in teams.iteritems():
					if a != 'lastupdate':
					#return bt+t1.strip()+nident+t2.strip()+mr.strip()+' '+status+bt
					#gm,color=False,showMr=False,score=True,branked=False,custformat='
						if c.lower() == b['team1'].lower() or c.lower()==b['team2'].lower():
							ta=gameInfo(a,True,False,True,False,'%BT%%T1% %NIDENT% %T2% %MR%%STATUS%%BT%',True).replace(' IN ',' ').replace('vs.','v').replace('HALFTIME','HALF').replace(' ET','').replace(' PM','PM').replace(' AM','AM')
							if not ta in conf: conf.append(ta)
		conf=', '.join(conf)
		conf=conf.strip()
		if len(conf) < 10: conf=''
		if conf != '':
			for a in splitMessage(conf):
				db['msgqueue'].append([a,dest,'PRIVMSG',None])
		else:
			if ''.join(params).lower().replace(' ','') == 'top25':
				topar=[]
				for a,b in db['games'].iteritems():
					if a != 'lastupdate':
						t1rk=26
						t2rk=26
						rks=artolower(db['ranks'])
						if b['team1'].lower() in rks: t1rk=rks[b['team1'].lower()]
						if b['team2'].lower() in rks: t2rk=rks[b['team2'].lower()]
						if t1rk==None: t1rk=26
						if t2rk==None: t2rk=26
						#print b['team1']+' '+str(t1rk)+' '+b['team2']+' '+str(t2rk)
						trk=26
						#print t1rk
						if int(t1rk) <= 25 or int(t2rk) <=25:
							if int(t1rk) < int(t2rk): trk=t1rk
							else: trk=t2rk
							topar.append({'game': a, 'rk': int(trk)})
				#print 'topar:'
				#print  topar
				topar=sorted(topar,key=lambda k: k['rk'])
				#print topar
				topar2=[]
				topvals=''
				for a in topar:
					topar2.append(gameInfo(a['game'],True,False,True,False,'%BT%%T1% %NIDENT% %T2% %MR%%STATUS%%BT%',True).replace(' IN ',' ').replace('vs.','v').replace('HALFTIME','HALF').replace(' ET','').replace(' PM','').replace(' AM',''))
				topvals=', '.join(topar2)
				#print 'tops:'+topvals
				for a in splitMessage(topvals,400,', '):
					db['msgqueue'].append([a,dest,'PRIVMSG',None])
			else:


				fcs=json.loads(sql.unique_get('data','fcs'))
				closests=''
				closestval=100
				for aa,bb in fcs.iteritems():
					if aa != 'lastupdate':
						team1=bb['team1'].lower().replace('(','').replace(')','')
						team2=bb['team2'].lower().replace('(','').replace(')','')
						if params.count(' ') == 0: tclv=closest([params.lower(),params.lower()+' StateZ',params.lower().replace('st','state')],[team1.lower(),team2.lower()])
						else: tclv=closest([params.lower(),params.lower().replace('st','state')],[team1.lower(),team2.lower(),team1.lower()+team2.lower(),team2.lower()+team1.lower()])
						if tclv < closestval:
							closestval=tclv
							closests=aa
				if dest=='footballbot' or dest=='footballtestbot': dest=origin

				if closests != '' and closestval <= 3:
					db['msgqueue'].append([gameInfo(closests,True,True,newdb=fcs)+'* '+shorten_url('http://sports.espn.go.com/ncf/boxscore?gameId='+fcs[closests]['gid'])+'*',dest,tmtype,'score'])					

					
				else:
					clv_isteam_val=100000
					clv_isteam_act=''
					for a,b in db['colors'].iteritems():
						clv_isteam=closest([params.lower(),params.replace('st','state').lower()],[a.lower()])
						if clv_isteam < clv_isteam_val:
							clv_isteam_val=clv_isteam
							clv_isteam_act=a
					if clv_isteam_val <=3:
						db['msgqueue'].append([origin+': '+clv_isteam_act+' has a bye week (or is not a FBS team).',dest,'PRIVMSG',None])
					else:
						numbers = re.compile('\d+(?:\.\d+)?')
						pnum=''.join(numbers.findall(params))
						pnum=pnum
						pnum=pnum[:-2]+':'+pnum[-2:]
						if len(pnum) ==4 or len(pnum)==5:
							conf=[]					
							for a,b in teams.iteritems():
								if a != 'lastupdate':
								#return bt+t1.strip()+nident+t2.strip()+mr.strip()+' '+status+bt
								#gm,color=False,showMr=False,score=True,branked=False,custformat='
									if b['status'].count(pnum) != 0 and b['status'].count('ET') != 0:
										ta=gameInfo(a,True,False,True,False,'%BT%%T1% %NIDENT% %T2% %MR% %NTWKS%%BT%',True).replace(' IN ',' ').replace('vs.','v').replace('HALFTIME','HALF').replace(' ET','').replace(' PM','PM').replace(' AM','AM')
										if not ta in conf: conf.append(ta.strip())
							conf=', '.join(conf)
							conf=conf.strip()
							if len(conf) < 10: conf=''
							if conf != '':
								db['msgqueue'].append([conf,dest,'PRIVMSG',None])
							else: db['msgqueue'].append([origin+': I can\'t find any games starting at '+pnum+'.',dest,'PRIVMSG',None])
								
						else:
							db['msgqueue'].append([origin+': I do not know what team you are referring to.',dest,'PRIVMSG',None])
		#[original_message,channel (all main chans), type(PRIVMSG),identifier(None)]
