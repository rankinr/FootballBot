lst=''
lstar=[]
ts=''
nextgames={}
status_replace={}
exec(open('/home/fbbot/cfb/common_functions.py')) #load custom functions
for b,a in db['games_new']['fbs'].iteritems():
	#print a
	if b != 'lastupdate':
		st=str(a['status']).lower()
		if st.count('pm et') != 0 or st.count('pm edt') != 0:
			stp=st.replace(' et','').replace(' edt','')
			yr=time.strftime('%Y')
			if st[:2] == '1/':
				yr=str(int(yr)+1)
			stp=time.mktime(time.strptime(stp+' '+yr,'%m/%d - %I:%M %p %Y'))
			status_replace[b]=[a['status'],'- '+time.strftime('%a',time.localtime(stp))+', '+st.replace(' edt','').upper()]
			if len(nextgames) < 50: nextgames[b]=stp
			else:
				mva=max(nextgames,key=nextgames.get)
				if stp < nextgames[mva]:
					nextgames.pop(mva)
					nextgames[b]=stp
		if st.count('final') == 0 and st.count('delay') == 0 and st.count('am et') == 0 and st.count('pm et') == 0 and st.count('am edt') == 0 and st.count('pm edt') == 0 and st.count('cancel') == 0:
			lstar.append(gameInfo(b,False, False, True, True, '', True).strip())
			if lst=='':
				lst+=gameInfo(b,branked=True,supershort=True).strip()
			else:
				lst+=' | '+gameInfo(b,branked=True,supershort=True).strip()
				ts+='PRIVMSG '+origin+' :'+lst+chr(3)+'\r\n'
#				db['msgqueue'].append([lst+chr(3),origin,'PRIVMSG'])
				#lst=''
nextgames = sorted(nextgames.iteritems(), key=operator.itemgetter(1))
lst=lst.strip()
if lst == '' and ts == '':
	lst='There are no games on at the moment. '
ngl=''
#print status_replace
last_game_time=''
today_time=time.localtime()
tomorrow_time=time.localtime(time.time()+3600*24)
today_date=str(today_time[1])+'/'+str(today_time[2])
tomorrow_date=str(tomorrow_time[1])+'/'+str(tomorrow_time[2])
for a in nextgames:
	if len(ngl) < 400:
		nass=a[0]
		this_time=db['games_new']['fbs'][nass]['status']
		this_time_first=this_time[:this_time.find(' - ')].strip()
		if this_time_first==today_date: this_time=this_time.replace(this_time_first,'Today')
		elif this_time_first==tomorrow_date: this_time=this_time.replace(this_time_first,'Tomorrow')
		this_game_add=gameInfo(nass,score=False,branked=True,supershort=True,showStatus=False).strip()
		if a[0] in status_replace: 
			#print 'replacing'
			this_game_add=this_game_add.replace(status_replace[a[0]][0],status_replace[a[0]][1])
		if last_game_time != this_time:
			if last_game_time != '': 
				ngl=ngl[:-2]
				ngl+='  |  '
			if last_game_time.count('Today') != 0 and this_time.count('Today') != 0: ngl+='\x02'+(this_time.replace(' - ','').replace(' ET','').replace('Today','')).strip()+'\x02: '
			else: ngl+='\x02'+this_time.replace(' - ',' at ').replace(' ET','')+'\x02: '
		ngl+=this_game_add+', '
		last_game_time=this_time
ngl=ngl[:-2]
send_ng=''
if len(nextgames) != 0 and (lst == 'There are no games on at the moment. ' or len (lstar) < 4): 
	send_ng='\x02Upcoming games: \x02'+ngl+'\r\n'
	comb=lst
else:
	comb=', '.join(lstar)

if dest.lower()=='footballbot': msg_dest=origin
else: msg_dest=dest

user_pref=sql.get_user(origin)
msg_type='PRIVMSG'
if user_pref:
	if 'cmds' in user_pref and 'whatson' in user_pref['cmds']:
		if user_pref['cmds']['whatson']=='you': msg_dest=origin
		elif user_pref['cmds']['whatson']=='channel' and dest.lower()!='footballbot': msg_dest=dest
	if 'pers_msgs' in user_pref and msg_dest==origin:
		if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
		elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'

for comb in splitMessage(comb,500,' | '):
	db['msgqueue'].append([comb,msg_dest,msg_type])
if send_ng != '':
	for comb in splitMessage(send_ng,500, ' | '):
		db['msgqueue'].append([comb,msg_dest,msg_type])