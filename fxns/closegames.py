lst=''
lste=''
ts=''
for b,a in db['games'].iteritems():
	#print a
	if b != 'lastupdate':
		st=str(a['status']).lower()
		if st.count('final') == 0 and st.count('delay') == 0 and st.count('am et') == 0 and st.count('pm et') == 0:
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
				if closests in db['ntwks']: ntwks=' - '+db['ntwks'][closests]
				if lst != '': lst+=' '+chr(3)+'1,1.'+chr(3)+' '
				(t1rk != '' and t2rk != '' and int(t2rk.replace('(','').replace(')','').strip()) > int(t1rk.replace('(','').replace(')','').strip()))
				if (   ((t1rk == '' and t2rk != '') or (t1rk != '' and t2rk != '' and int(t1rk.replace('(','').replace(')','').strip()) > int(t2rk.replace('(','').replace(')','').strip()))) and int(ourgame['team1score']) >= int(ourgame['team2score'])) or (((      ((t2rk == '' and t1rk != '') or ((t1rk != '' and t2rk != '' and int(t2rk.replace('(','').replace(')','').strip()) > int(t1rk.replace('(','').replace(')','').strip())))) and int(ourgame['team2score']) >= int(ourgame['team1score'])))):
					lst+=chr(3)+'0,4UPSET ALERT: '
					lste=chr(3)
				lst+=t1+'-'+t2+' ('+ourgame['status']+ntwks+')'+lste
if dest == 'footballbot': dest=origin
if lst != '': ts+='PRIVMSG '+dest+' :'+lst+chr(3)+'\r\n'

#db['msgqueue'].append([lst+chr(3),origin,'PRIVMSG'])
s.send(ts)
