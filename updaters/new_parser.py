"""Back to the basics with this one. Gets the current status of games,
sends messages to the channel if there are changes to the score, and
sends messages to users who requested updates if there are changes to
the status.

Runs every five minutes. If all the games are over, will quit after it checks once; otherwise, it will run every 8-12 seconds for about five minutes."""
import urllib,time,random,re,traceback
import os,json,sys
from bs4 import BeautifulSoup
start_time=time.time()
from collections import OrderedDict
exec(open('/home/fbbot/cfb/common_functions.py').read())
exec(open('/home/fbbot/cfb/sload.py').read())
msgs_already_sent=[]
scores_already_sent=[]
prefix=''
db={}
db['teams']=json.loads(sql.unique_get('data','teams'))
db['shorten']=json.loads(sql.unique_get('data','shorten'))
db['logos']=json.loads(sql.unique_get('data','logos'))
scores_already_sent=json.loads(sql.unique_get('data','scores_sent'))
shorts=artolower(db['shorten'])
db['colors']=json.loads(sql.unique_get('data','colors'))
db['spread']=json.loads(sql.unique_get('data','spread'))
db['ntwks']=json.loads(sql.unique_get('data','ntwks'))
cis=artolower(db['colors'])
color_list=db['colors']
lastGames=json.loads(sql.unique_get('data','games_new')) #when you loop this, you can just run this at the beginning, then thereafter use the variable from the last run
for a in ['div2','fbs','fcs']:
	if not a in lastGames: lastGames[a]={}
#lastGames={'fbs':{},'fcs':{}}
db['games_new']=lastGames
rks=artolower(json.loads(sql.unique_get('data','ranks')))


logos=artolower(db['logos'].copy())
#logos={} #switch comment on these two lines during bowl games to have the bot announce logos when a team wins

colors={'white':'0','black':'1','blue':'2','green':'3','red':'4','maroon':'5','purple':'6','orange':'7','yellow':'8','light green':'9','teal':'10','cyan':'11','light blue':'12','pink':'13','grey':'14','silver':'15'}




start_load_updates=time.time()

sql.cur.execute("""select username,following from me;""" )
a=sql.cur.fetchall()

list_of_updates={}

teams_to_games={}
for game in db['games_new']['fbs']:
	teams_to_games[db['games_new']['fbs'][game]['team1']]=game
	teams_to_games[db['games_new']['fbs'][game]['team2']]=game
for game in db['games_new']['fcs']:
	teams_to_games[db['games_new']['fcs'][game]['team1']]=game
	teams_to_games[db['games_new']['fcs'][game]['team2']]=game
	
for user in a: #user[0] = username, [1] = following
	if user[1].strip() != '':
		uinfo=json.loads(user[1])
		for team in uinfo['teams']:
			if team in teams_to_games:
				if not teams_to_games[team] in list_of_updates:
					list_of_updates[teams_to_games[team]]=[]
				if not user[0] in   list_of_updates[teams_to_games[team]]: list_of_updates[teams_to_games[team]].append(user[0])
		for game in uinfo['this_week']:
			if not game in list_of_updates:
				list_of_updates[game]=[]
			if not user[0] in   list_of_updates[game]: list_of_updates[game].append(user[0])
#print list_of_updates
#print 'Total time to load users to update: '+str(time.time()-start_load_updates)
#print list_of_updates





keepGoing=True
nfl=getGameInfo('NA','http://espn.go.com/nfl/scoreboard') #not in the loop because only want it to update once every ~5 mins
nba=getGameInfo('NA','http://espn.go.com/nba/scoreboard') #not in the loop because only want it to update once every ~5 mins
#mlb=getGameInfo('NA','http://espn.go.com/mlb/scoreboard') #not in the loop because only want it to update once every ~5 mins
mlb=lastGames['mlb']
div2=getGameInfo('35')
#fcs=getGameInfo('81') SWITCH THESE OUT AT START OF NEXT SEASON
fcs=getGameInfo('bowl','http://espn.go.com/college-football/scoreboard/_/group/81/year/2015/seasontype/3/week/1')
try:
	while keepGoing:
		play_updates=[]
		#Get our games
		games={}
		games['fcs']=fcs
		#games['fbs']=getGameInfo('80')
		games['fbs']=getGameInfo('bowl','http://espn.go.com/college-football/scoreboard/_/group/80/year/2015/seasontype/3/week/1') #THIS AND NEXT LINE FOR BOWL SEASON
		#games['fbs'].update(getGameInfo('bowl','http://espn.go.com/college-football/scoreboard/_/group/80/year/2015/seasontype/2/week/15'))
		games['div2']=div2
		games['nfl']=nfl
		games['nba']=nba
		games['mlb']=mlb
		games['lastupdate']=int(time.time())
		isChange=False
		isChangefbs=False
		for l_type in games:
			if not l_type in lastGames or (l_type != 'lastupdate' and games[l_type] != lastGames[l_type]):
				if l_type=='fbs': isChangefbs=True
				isChange=True
		if isChange:
			for gid, gddt in games['fbs'].iteritems():
				if not 'odds' in gddt and gid in lastGames['fbs'] and 'odds' in lastGames['fbs'][gid]: games['fbs'][gid]['odds']=lastGames['fbs'][gid]['odds']
			for prefix in ['','ERN_']: sql.unique_set('data','games_new',json.dumps(games),prefix)
			#see if anything has changed for fbs teams. if so, send appropriate message
			for gid,gddt in games['fbs'].iteritems():
				st=gddt['status'].strip()
				score_code=gddt['team1']+gddt['team2']+gddt['team1score']+gddt['team2score']
				st=gddt['status'].strip().replace('EST','EDT')
				st=st.replace('15:00','BEGIN').replace(' IN ',' ')
				t1name=gddt['team1']
				t2name=gddt['team2']
				if t1name.lower() in shorts and shorts[t1name.lower()].strip() != '': t1name=shorts[t1name.lower()]
				if t2name.lower() in shorts and shorts[t2name.lower()].strip() != '': t2name=shorts[t2name.lower()]
				t1=t1name
				t2=t2name
				t1rk=''
				t2rk=''
				if gddt['team1'].lower() in rks and rks[gddt['team1'].lower()] != None: t1rk='('+rks[gddt['team1'].lower()]+') '
				if gddt['team2'].lower() in rks and rks[gddt['team2'].lower()] != None: t2rk='('+rks[gddt['team2'].lower()]+') '
				t1=t1rk+t1+' '+gddt['team1score']
				t2=t2rk+t2+' '+gddt['team2score']
				ntwkadd=''
				comm2=''
				poss=''
				mrcur=gddt['most_recent_play']
				if gid in lastGames['fbs'] and (int(gddt['team2score']) > int(lastGames['fbs'][gid]['team2score']) or int(gddt['team1score']) > int(lastGames['fbs'][gid]['team1score'])):
					print '1'
					if int(gddt['team2score']) > int(lastGames['fbs'][gid]['team2score']):
						print '2'
						if int(gddt['team2score']) == int(lastGames['fbs'][gid]['team2score'])+3: comm2=gddt['team2']+' Field Goal GOOD.'
						elif int(gddt['team2score']) == int(lastGames['fbs'][gid]['team2score'])+6: comm2=gddt['team2']+' Touchdown.'
						elif int(gddt['team2score']) == int(lastGames['fbs'][gid]['team2score'])+7: comm2=gddt['team2']+' Touchdown and Extra Point GOOD.'
						elif int(gddt['team2score']) == int(lastGames['fbs'][gid]['team2score'])+8: comm2=gddt['team2']+' Touchdown and Two Point Conversion.'
						elif int(gddt['team2score']) == int(lastGames['fbs'][gid]['team2score'])+2: comm2=gddt['team2']+' Score.'
						elif int(gddt['team2score']) == int(lastGames['fbs'][gid]['team2score'])+1: comm2=gddt['team2']+' Extra Point GOOD.'
					if int(gddt['team1score']) > int(lastGames['fbs'][gid]['team1score']):
						print '3'
						if int(gddt['team1score']) == int(lastGames['fbs'][gid]['team1score'])+3: comm2=gddt['team1']+' Field Goal GOOD.'
						elif int(gddt['team1score']) == int(lastGames['fbs'][gid]['team1score'])+6: comm2=gddt['team1']+' Touchdown.'
						elif int(gddt['team1score']) == int(lastGames['fbs'][gid]['team1score'])+7: comm2=gddt['team1']+' Touchdown and Extra Point GOOD.'
						elif int(gddt['team1score']) == int(lastGames['fbs'][gid]['team1score'])+8: comm2=gddt['team1']+' Touchdown and Two Point Conversion.'
						elif int(gddt['team1score']) == int(lastGames['fbs'][gid]['team1score'])+2: comm2=gddt['team1']+' Score.'
						elif int(gddt['team1score']) == int(lastGames['fbs'][gid]['team1score'])+1: comm2=gddt['team1']+' Extra Point GOOD.'
					#print comm2
					poss=gddt['possession']
				comm2=comm2+' '+mrcur.strip()
				if poss != None:
					if poss.lower() == t1name.lower(): t1=t1+' (:)'
					elif poss.lower() == t2name.lower(): t2=t2+' (:)'
				if gddt['team1'].lower() in cis: t1=chr(3)+str(cis[gddt['team1'].lower()][0])+','+str(cis[gddt['team1'].lower()][1])+t1.strip()+chr(3)
				if gddt['team2'].lower() in cis: t2=chr(3)+str(cis[gddt['team2'].lower()][0])+','+str(cis[gddt['team2'].lower()][1])+t2.strip()+chr(3)
				if gddt['team1'] in irc_flairs: t1='*'+chr(3)+irc_flairs[gddt['team1']][0]+chr(3)+irc_flairs[gddt['team1']][1]+chr(3)+irc_flairs[gddt['team1']][3]+chr(3)+irc_flairs[gddt['team1']][4]+chr(3)+'*'+t1 # flair compatibility with custom version of kiwi
				if gddt['team2'] in irc_flairs: t2='*'+chr(3)+irc_flairs[gddt['team2']][0]+chr(3)+irc_flairs[gddt['team2']][1]+chr(3)+irc_flairs[gddt['team2']][3]+chr(3)+irc_flairs[gddt['team2']][4]+chr(3)+'*'+t2
				oinfo=[]
				if st.count('BEGIN') == 1 and st.count('1st') == 1:
					if gid in db['ntwks']: ntwkadd=' - '+db['ntwks'][gid]
					if 'odds' in gddt: oinfo.append('\x02Spread\x02: '+gddt['odds'])
					if 'temperature' in gddt and gddt['temperature'] != '': oinfo.append('\x02Weather:\x02 '+gddt['temperature'])
					if 'location' in gddt and gddt['location'] != '': oinfo.append('\x02Location:\x02 '+gddt['location'].strip())
				oinfo=', '.join(oinfo).strip()
				if comm2 == '':
					datm=''
					datmn=''
					if gid in lastGames and gddt['team2score'] != lastGames['fbs'][gid]['team2score']:
						datm=gddt['team2']
						datmn='team2'
					elif gid in lastGames and gddt['team1score'] != lastGames['fbs'][gid]['team1score']:
						datm=gddt['team1']
						datmn='team1'
					if datm != '':
						dacomm=''
						if gddt[datmn+'score'] == int(lastGames['fbs'][gid][datmn+'score'])+6: dacomm=datm+' TOUCHDOWN!'
						if gddt[datmn+'score'] == int(lastGames['fbs'][gid][datmn+'score'])+3: dacomm=datm+' FIELD GOAL!'
						if gddt[datmn+'score'] == int(lastGames['fbs'][gid][datmn+'score'])+1: dacomm=datm+' EXTRA POINT GOOD!'
						if dacomm != '': comm2=dacomm
				stats_to_append=''
				logo=[]
				if (st.upper().count('FINAL') == 1 or st.upper().count('HALF') == 1) and gid in lastGames['fbs'] and lastGames['fbs'][gid]['status'].upper().count('FINAL')+lastGames['fbs'][gid]['status'].upper().count('HALF') == 0:
					#print 'yes'
					sts=stats(gddt['gid'])
					stats_to_append=' -- GAME STATS: '+sts+chr(3)
					winningteam='THISISADEFAULTVALUE'
					if int(gddt['team1score']) > int(gddt['team2score']): winningteam=gddt['team1']
					elif int(gddt['team2score']) > int(gddt['team1score']): winningteam=gddt['team2']
					jfbs=json.dumps(games['fbs']).upper()
					if len(games['fbs'])-jfbs.count('PM ET')-jfbs.count('AM ET')-jfbs.count('FINAL') < 5 and st.upper().count('FINAL') == 1 and winningteam.lower() in logos:
						lines=logos[winningteam.lower()].split('\r\n')
						tosend=[]
						for line in lines:
							while line.count('(') != 0:
								paren=line[line.find('(')+1:line.find(')')]
								col1=paren[:paren.find(',')].strip().lower()
								col2=paren[paren.find(',')+1:].strip().lower()
								if col1 in colors: col1=colors[col1]
								else: col1=0
								if col2 in colors: col2=colors[col2]
								else: col2=0
								line=line[:line.find('(')]+chr(3)+col1+','+col2+line[line.find(')')+1:]
							tosend.append(chr(3)+'0,0.'+line)
						logo=tosend
					if st.upper().count('FINAL') == 1:
						bets=json.loads(sql.unique_get('data','bets'))
						cash=json.loads(sql.unique_get('data','cash'))
						doupdate=False
						db['msgqueue']=json.loads(sql.unique_get('data','msgqueue'))
						for user, betinfo in bets.iteritems():
							if gid in betinfo:
								doupdate=True
								if betinfo[gid][0]==gddt['team1']:
									onteam='team1'
									againstteam='team2'
								elif betinfo[gid][0]==gddt['team2']:
									onteam='team2'
									againstteam='team1'
								if betinfo[gid][1][0]=='+':
									if float(gddt[againstteam+'score'])-float(gddt[onteam+'score']) < float(betinfo[gid][1][1:]): win=True
									else: win=False
								elif betinfo[gid][1][0]=='-':
									if float(gddt[onteam+'score'])-float(gddt[againstteam+'score']) > float(betinfo[gid][1][1:]): win=True
									else: win=False
								if win: 
									cash[user]=round(cash[user]+betinfo[gid][2]*2,2) # x2 to reimburse original pay in
									db['msgqueue'].append(['Congratulations! '+betinfo[gid][0]+' covered the spread, so you have won $'+cashVal(betinfo[gid][2])+'. Your wallet contains $'+cashVal(cash[user])+'.',user,'PRIVMSG'])
								else:
									db['msgqueue'].append(['Oh no! You just lost $'+cashVal(betinfo[gid][2])+' because '+betinfo[gid][0]+' didn\'t cover the spread! Your wallet contains $'+cashVal(cash[user])+'.',user,'PRIVMSG'])
								bets[user].pop(gid)
						if doupdate:
							sql.unique_set('data','bets',json.dumps(bets))
							sql.unique_set('data','cash',json.dumps(cash))
							sql.unique_set('data','msgqueue',json.dumps(db['msgqueue']))
				if comm2.strip() != '': comm2=' '+comm2
				if gddt['neutral'] == True: cnctr='-'
				else: cnctr=' @ '
				if oinfo != '': oinfo=' - '+oinfo
				msg='\x02'+t1+' '+cnctr+' '+t2+'\x02'+comm2+' ('+st+ntwkadd+')'+stats_to_append+oinfo
				#new plays (for users requesting that info)
				#if gid in lastGames['fbs'] and gddt['most_recent_play'] != lastGames['fbs'][gid]['most_recent_play'] and gddt['most_recent_play'] != '':
				#	db['msgqueue']=json.loads(sql.unique_get('data','msgqueue'))
				#	db['msgqueue'].append([msg,'harkatmuld','NOTICE',None])
				#	sql.unique_set('data','msgqueue',json.dumps(db['msgqueue']))
				#new scores/big changes
				if gid in lastGames['fbs'] and gddt != lastGames['fbs'][gid]:
					if gddt['most_recent_play'] != lastGames['fbs'][gid]['most_recent_play'] and gid in list_of_updates:
						play_updates.append(gid)
					if gid.count('Memphis') == 0 and (((gddt['status'].upper().count('FINAL')==1  or gddt['status'].upper().count('OT') == 1 or gddt['status'].upper().count('15:00') != 0 or gddt['status'].upper().count('HALFTIME') != 0) and gddt['status'] != lastGames['fbs'][gid]['status']) or ((int(gddt['team1score']) > int(lastGames['fbs'][gid]['team1score'])	or int(gddt['team2score']) > int(lastGames['fbs'][gid]['team2score'])) and not score_code in scores_already_sent)):				
						if not msg in msgs_already_sent:
							db['msgqueue']=json.loads(sql.unique_get('data','msgqueue'))
							if len(logo) > 0:
								for logo_line in logo:
									db['msgqueue'].append([logo_line,None,None,'score'])
							db['msgqueue'].append([msg,None,None,'score']) #when make it final, update to [msg,None,None,'score']
							sql.unique_set('data','msgqueue',json.dumps(db['msgqueue']))
							msgs_already_sent.append(msg)
							scores_already_sent.append(score_code)
			for gid,gddt in games['fcs'].iteritems():
				if gid in lastGames['fcs'] and gddt != lastGames['fcs'][gid] and gddt['most_recent_play'] != lastGames['fcs'][gid]['most_recent_play'] and gid in list_of_updates:
					play_updates.append(gid)
		j_string=json.dumps(games['fbs']).upper()
		if j_string.count('TEAM1SCORE') == j_string.count('PM ET')+j_string.count('AM ET') or j_string.count('TEAM1SCORE') == j_string.count('DELAYED')+j_string.count('PM ET')+j_string.count('AM ET')+j_string.count('FINAL'):
			start_time=0

		if time.time() > start_time+60*4.5:
			keepGoing=False
		lastGames=games
		if len(play_updates) > 0:
			play_updates_f={}
			for game in play_updates:
				play_updates_f[game]=list_of_updates[game]
			#print play_updates_f
			sql.unique_set('data','play_updates',json.dumps(play_updates_f))
		time.sleep(random.randrange(12,16))
	sql.unique_set('data','scores_sent',json.dumps(scores_already_sent))
except:
	errr=str(traceback.format_exc().replace('\n',''))
	errr=errr[errr.find(':')+2:]
	errors=json.loads(sql.unique_get('data','errors'))
	if errr in errors: errors[errr][0]+=1
	else: errors[errr]=[1,0]
	errors[errr][1]=time.time()
	print errr
	sql.unique_set('data','errors',json.dumps(errors))	
sql.unique_set('data','scores_sent',json.dumps(scores_already_sent))