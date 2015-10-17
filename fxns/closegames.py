lst=''
lste=''
ts=''
if dest.lower()=='footballbot': msg_dest=origin
else: msg_dest=dest

user_pref=sql.get_user(origin)
msg_type='PRIVMSG'
if user_pref:
	if 'cmds' in user_pref and 'closegames' in user_pref['cmds']:
		if user_pref['cmds']['closegames']=='you': msg_dest=origin
		elif user_pref['cmds']['closegames']=='channel' and dest.lower()!='footballbot': msg_dest=dest
	if 'pers_msgs' in user_pref and msg_dest==origin:
		if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
		elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'


for b,a in db['games_new']['fbs'].iteritems():
	if b != 'lastupdate':
		st=str(a['status']).lower()
		if st.count('final') == 0 and st.count('delay') == 0 and st.count('am edt') == 0 and st.count('pm edt') == 0:
			ourgame=a
			t1rk=''
			t2rk=''
			rks=artolower(db['ranks'])
			if ourgame['team1'].lower() in rks and rks[ourgame['team1'].lower()] != None: t1rk='('+rks[ourgame['team1'].lower()]+') '
			if ourgame['team2'].lower() in rks and rks[ourgame['team2'].lower()] != None: t2rk='('+rks[ourgame['team2'].lower()]+') '
			if st.count('1st') == 0 and ((   ((t1rk == '' and t2rk != '') or (t1rk != '' and t2rk != '' and int(t1rk.replace('(','').replace(')','').strip()) > int(t2rk.replace('(','').replace(')','').strip()))) and int(ourgame['team1score']) >= int(ourgame['team2score'])) or (((      ((t2rk == '' and t1rk != '') or ((t1rk != '' and t2rk != '' and int(t2rk.replace('(','').replace(')','').strip()) > int(t1rk.replace('(','').replace(')','').strip())))) and int(ourgame['team2score']) >= int(ourgame['team1score'])) or abs(int(ourgame['team2score'])-int(ourgame['team1score'])) < 7))):
				t1=ourgame['team1']
				t2=ourgame['team2']
				t1=t1rk+t1+' '+ourgame['team1score']
				t2=t2rk+t2+' '+ourgame['team2score']
				tmtype='PRIVMSG'
				ntwks=''
				closests=b
				if closests in db['ntwks'] and db['ntwks'][closests].strip() != '': ntwks=' - '+db['ntwks'][closests].strip()
				if lst != '': lst+=' '+chr(3)+'1,1 . '+chr(3)+' '
				(t1rk != '' and t2rk != '' and int(t2rk.replace('(','').replace(')','').strip()) > int(t1rk.replace('(','').replace(')','').strip()))
				if (   ((t1rk == '' and t2rk != '' and int(t2rk.replace('(','').replace(')','').strip()) < 50) or (t1rk != '' and t2rk != '' and int(t1rk.replace('(','').replace(')','').strip()) > int(t2rk.replace('(','').replace(')','').strip()) and (int(t2rk.replace('(','').replace(')','').strip()) < 25 or int(t1rk.replace('(','').replace(')','').strip())-int(t2rk.replace('(','').replace(')','').strip()) > 15)      )) and int(ourgame['team1score']) >= int(ourgame['team2score'])) or (((      ((t2rk == '' and t1rk != '' and int(t1rk.replace('(','').replace(')','').strip()) < 50) or ((t1rk != '' and t2rk != '' and int(t2rk.replace('(','').replace(')','').strip()) > int(t1rk.replace('(','').replace(')','').strip()) and (  (int(t1rk.replace('(','').replace(')','').strip()) < 25) or (int(t2rk.replace('(','').replace(')','').strip())-int(t1rk.replace('(','').replace(')','').strip()) > 15)  ) ))) and int(ourgame['team2score']) >= int(ourgame['team1score'])))):
					lst+=chr(3)+'0,4UPSET ALERT: '
					lste=chr(3)
				lst+=t1+'-'+t2+' ('+ourgame['status']+ntwks+')'+lste
if dest == 'footballbot': dest=origin
if lst != '': ts+='PRIVMSG '+dest+' :'+lst+chr(3)+'\r\n'
print 'end'
#db['msgqueue'].append([lst+chr(3),origin,'PRIVMSG'])
#s.send(ts)
lst=lst.strip()
if lst != '':
	for msg in splitMessage(lst,400,' . '):
		db['msgqueue'].append([msg,msg_dest,msg_type])