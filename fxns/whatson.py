<<<<<<< HEAD
lst=''
lstar=[]
ts=''
nextgames={}
for b,a in db['games'].iteritems():
	#print a
	if b != 'lastupdate':
		st=str(a['status']).lower()
		if st.count('pm et') != 0:
			stp=st.replace(' et','')
			yr=time.strftime('%Y')
	                if st.count('jan') != 0: yr=str(int(yr)+1)
			stp=time.mktime(time.strptime(stp+' '+yr,'%a, %b %d %I:%M %p %Y'))
			if len(nextgames) < 11: nextgames[b]=stp
			else:
				mva=max(nextgames,key=nextgames.get)
				if stp < nextgames[mva]:
					nextgames.pop(mva)
					nextgames[b]=stp
		if st.count('final') == 0 and st.count('delay') == 0 and st.count('am et') == 0 and st.count('pm et') == 0 and st.count('cancel') == 0:
			lstar.append(gameInfo(b,False, False, True, True, '', True))
			if lst=='':
				lst+=gameInfo(b,branked=True)
			else:
				lst+=' '+chr(3)+'0,1 . '+chr(3)+' '+gameInfo(b,branked=True)
				ts+='PRIVMSG '+origin+' :'+lst+chr(3)+'\r\n'
#				db['msgqueue'].append([lst+chr(3),origin,'PRIVMSG'])
				lst=''
=======
lst = ''
lstar = []
ts = ''
nextgames = {}
for b, a in db['games'].iteritems():
    #print a
    if b != 'lastupdate':
        st = str(a['status']).lower()
        if st.count('pm et') != 0:
            stp = st.replace(' et', '')
            yr = time.strftime('%Y')
            if st.count('jan') != 0: yr = str(int(yr) + 1)
            stp = time.mktime(time.strptime(stp + ' ' + yr,
                                            '%a, %b %d %I:%M %p %Y'))
            if len(nextgames) < 10: nextgames[b] = stp
            else:
                mva = max(nextgames, key=nextgames.get)
                if stp < nextgames[mva]:
                    nextgames.pop(mva)
                    nextgames[b] = stp
        if st.count('final') == 0 and st.count('delay') == 0 and st.count(
                'am et') == 0 and st.count('pm et') == 0 and st.count(
                        'cancelled') == 0:
            lstar.append(gameInfo(b, False, False, True, True, '', True))
            if lst == '':
                lst += gameInfo(b, branked=True)
            else:
                lst += ' ' + chr(3) + '0,1 . ' + chr(3) + ' ' + gameInfo(
                    b,
                    branked=True)
                ts += 'PRIVMSG ' + origin + ' :' + lst + chr(3) + '\r\n'
                #				db['msgqueue'].append([lst+chr(3),origin,'PRIVMSG'])
                lst = ''
>>>>>>> origin/master
nextgames = sorted(nextgames.iteritems(), key=operator.itemgetter(1))
lst=lst.strip()
if lst == '' and ts == '':
<<<<<<< HEAD
	lst='There are no games on at the moment. '
	if dest.lower() != 'footballbot': origin=dest
ngl=''
for a in nextgames:
	nass=a[0]
	ngl+=gameInfo(nass,score=False,branked=True)+', '
ngl=ngl[:-2]
if len(nextgames) != 0 and lst == 'There are no games on at the moment. ': 
	lst+='\x02Upcoming games: \x02'+ngl+'\r\n'
	comb=lst
else:
	comb=', '.join(lstar)
if dest=='footballbot': dest=origin
for comb in splitMessage(comb,400,' . '):
	db['msgqueue'].append([comb,dest])
=======
    lst = 'There are no games on at the moment.'
    if dest.lower() != 'footballbot': origin = dest
if lst != '': ts += 'PRIVMSG ' + origin + ' :' + lst + chr(3) + '\r\n'
ngl = ''
for a in nextgames:
    nass = a[0]
    ngl += gameInfo(nass, score=False, branked=True) + ', '
ngl = ngl[:-2]
if len(nextgames) != 0:
    ts += 'PRIVMSG ' + origin + ' :\x02Upcoming games: \x02' + ngl + '\r\n'
comb = ', '.join(lstar)
if dest == 'footballbot': dest = origin
for comb in sMsg(comb, 400, ' . '):
    db['msgqueue'].append([comb, dest])
>>>>>>> origin/master
