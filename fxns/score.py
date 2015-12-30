"""Looks up games by team name ("!score UMiami"), conference ("!score ACC") or time ("!score 330").
"score" can be omitted (i.e., "!UMiami", "!ACC", or "!330" will produce the same results as above)""" 
#exec(open('/home/fbbot/cfb/common_functions.py')) #load custom functions
un_team=False
newo=''
st_t=''
if isText: st_t=origin+': '
if (origin.count('|') != 0 or origin.count('[') != 0):
	if origin.count('|') != 0: newo=origin[origin.find('|')+1:]
	elif origin.count('[') != 0: 
		newo=origin[origin.find('[')+1:]
		if newo.count(']') != 0: newo=newo[:newo.find(']')]
	if  ''.join(params).strip() == '' and newo.strip() != '': params=[newo.strip()]
	if newo.strip() != '': un_team=match(newo)
team_list=[]
for team in db['teams']: team_list.append(team.lower())
if dest.lower()=='footballbot': msg_dest=origin
else: msg_dest=dest
bye=False
closest_bye_alt=''
user_pref=sql.get_user(origin)
msg_type='PRIVMSG'
short_params=''.join(params).lower().replace(' ','')
if short_params in abbrev_lower:
	params=abbrev_lower[short_params].split(' ')
	short_params=''.join(params).lower().replace(' ','')
if user_pref:
	if 'cmds' in user_pref and 'score' in user_pref['cmds']:
		if user_pref['cmds']['score']=='you': msg_dest=origin
		elif user_pref['cmds']['score']=='channel' and dest.lower()!='footballbot': msg_dest=dest
	if 'pers_msgs' in user_pref and msg_dest==origin:
		if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
		elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'
if ''.join(params).strip() != '':
	if short_params=='nfl' or short_params=='nba' or short_params=='mlb' or short_params=='football' or short_params=='baseball' or short_params=='basketball' or short_params=='fcs':
		if short_params=='football':short_params='nfl'
		if short_params=='nba':short_params='nba'
		if short_params=='mlb':short_params='mlb'
		list_of_teams=[]
		#print db['games_new'][short_params]
		for a,b in db['games_new'][short_params].iteritems():
			if b['status'].count(' PM ') == 0 and b['status'].count(' AM ') == 0: list_of_teams.append(gameInfo(a,True,False,True,False,'%BT%%T1% %NIDENT% %T2% %MR%%STATUS%%BT%').replace(' IN ',' ').replace('vs.','v').replace('HALFTIME','HALF').replace(' ET','').replace(' PM','PM').replace(' AM','AM'))
		#print splitMessage(' | '.join(list_of_teams).encode('utf8'))
		print 'a'
		for msg in splitMessage(' | '.join(list_of_teams).encode('utf8'),400,'|'):
			db['msgqueue'].append([msg,msg_dest,msg_type,'score'])
	else:
		tbyname={}
		closestval=1000000
		closests=''
		teams=db['games_new']['fbs'].copy()
		for l_type in db['games_new']:
			if l_type != 'lastupdate' and l_type != 'fbs': teams.update(db['games_new'][l_type])
		params=' '.join(params).lower()
		print params
		#print '1:'+params
		params_orig=params
		#print '2:'+params_orig
		if not params in team_list and not params in conf_lower: params=abbrev(params,db['abbreviations'])
		#print '3:'+params
		#print '4:'+params_orig
		for a,b in teams.iteritems():
			if a != 'lastupdate':
				team1=b['team1'].lower().replace('(','').replace(')','')
				team2=b['team2'].lower().replace('(','').replace(')','')
				if params.count(' ') == 0: tclv=closest([params_orig,params.lower(),params.lower()+' StateZ',params.lower().replace('st','state')],[team1.lower(),team2.lower()])
				else: tclv=closest([params_orig,params.lower(),params.lower().replace('st','state')],[team1.lower(),team2.lower(),team1.lower()+team2.lower(),team2.lower()+team1.lower()])
				if tclv < closestval:
					closestval=tclv
					closests=a
		#print closestval
		#print closests
		#print 'params:'+params+'.'+params_orig
		if params in conf_lower:
			closestval=1000
		bye=False
		if closestval != 0 and params_orig in team_list:
			bye=True
			params=params_orig
			closest_bye_alt=''
			if closestval <= 3: closest_bye_alt=closests
			closests=''
		elif closestval != 0 and params_orig.lower().replace(' ','') in conf_lower:
			closestval=100
			closests=''
		if dest=='footballbot' or dest=='footballtestbot': dest=origin
		if (closests != '' and closestval <= 3 and not isAutoDetect) or (closests != '' and ((len(params) > 5 and closestval <=3) or (len(params) <= 2 and closestval < 1) or (len(params) <= 5 and closestval <= 1))):
			oinfo=[]
			if teams[closests]['status'].count(' ET') != 0:
				if 'odds' in teams[closests]: oinfo.append('\x02Spread\x02: '+teams[closests]['odds'])
				if 'temperature' in teams[closests] and teams[closests]['temperature'] != '': oinfo.append('\x02Weather:\x02 '+teams[closests]['temperature'])
				if 'location' in teams[closests] and teams[closests]['location'] != '': oinfo.append('\x02Location:\x02 '+teams[closests]['location'].strip())
			oinfo=', '.join(oinfo)
			if oinfo != '': oinfo='- '+oinfo
			if not isText: type_of_text=''
			if isAutoDetect==False or lastAutoDetect != closests or time.time()-lastAutoDetectTime > 5:
				lastAutoDetect=closests
				lastAutoDetectTime=time.time()
				s_url=''
				if closests in db['games_new']['fbs'] or closests in db['games_new']['fcs']: 
					if dest == '#redditcfb': s_url='' 
					else: s_url=shorten_url('http://sports.espn.go.com/ncf/boxscore?gameId='+teams[closests]['gid'])
				db['msgqueue'].append([st_t+gameInfo(closests,True,True,typ_of_text=type_of_text,ircFlair=True)+'* '+s_url+' *'+oinfo,msg_dest,msg_type,'score'])
		else:
			conf=[]
			closest_conf=''
			closest_conf_val=100000
			for a,b in db['conferences'].iteritems():
				#print a
				#print params
				clv_conf=closest([params.lower()],[a.lower()])
				if clv_conf  < closest_conf_val:
					closest_conf_val=clv_conf
					closest_conf=a
			#db['msgqueue'].append([closest_conf+str(closest_conf_val),'harkatmuld','PRIVMSG'])
			#print closest_conf
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
			conf=' | '.join(conf)
			conf=conf.strip()
			if len(conf) < 10: conf=''
			if conf != '':
				#print conf
				for a in splitMessage(conf,'|'):
					db['msgqueue'].append([st_t+a,msg_dest,msg_type,None])
			else:
				if short_params == 'top25':
					topar=[]
					for a,b in db['games_new']['fbs'].iteritems():
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
						db['msgqueue'].append([a,msg_dest,msg_type,None])
				else:
					clv_isteam_val=100000
					clv_isteam_act=''
					for a,b in db['colors'].iteritems():
						clv_isteam=closest([params.lower(),params.replace('st','state').lower()],[a.lower()])
						if clv_isteam < clv_isteam_val:
							clv_isteam_val=clv_isteam
							clv_isteam_act=a
					if clv_isteam_val <=3:
						#print closest_bye_alt
						extra=''
						if bye and closest_bye_alt.strip() != '': extra=' (Did you mean '+gameInfo(closest_bye_alt)+'?)'
						db['msgqueue'].append([origin+': '+clv_isteam_act+' has a bye week.'+extra,msg_dest,msg_type,None])
					else:
						numbers = re.compile('\d+(?:\.\d+)?')
						pnum=''.join(numbers.findall(params))
						pnum=pnum
						pnum=pnum[:-2]+':'+pnum[-2:]
						#print pnum
						if len(pnum) ==4 or len(pnum)==5:
							conf=[]					
							for a,b in teams.iteritems():
								if a != 'lastupdate' and a in db['games_new']['fbs']:
								#return bt+t1.strip()+nident+t2.strip()+mr.strip()+' '+status+bt
								#gm,color=False,showMr=False,score=True,branked=False,custformat='
									if b['status'].count(pnum) != 0 and b['status'].count(' ET') != 0:
										ta=gameInfo(a,True,False,True,False,'%BT%%T1% %NIDENT% %T2% %MR% %NTWKS%%BT%',True).replace(' IN ',' ').replace('vs.','v').replace('HALFTIME','HALF').replace(' ET','').replace(' PM','PM').replace(' AM','AM')
										if not ta in conf: conf.append(ta.strip())
							conf=', '.join(conf)
							conf=conf.strip()
							if len(conf) < 10: conf=''
							if conf != '':
								for msg in splitMessage(conf,400,', '):
									db['msgqueue'].append([msg,msg_dest,msg_type,None])
							else: db['msgqueue'].append([origin+': I can\'t find any games starting at '+pnum+'.',msg_dest,msg_type,None])
								
						#else:
							#if isText==False: db['msgqueue'].append([origin+': I do not know what team you are referring to.',msg_dest,msg_type,None])
		#[original_message,channel (all main chans), type(PRIVMSG),identifier(None)]
