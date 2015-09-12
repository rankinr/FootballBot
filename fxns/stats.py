"""
Returns stats for game.
"""
<<<<<<< HEAD
if (origin.count('|') != 0 or origin.count('[') != 0) and ''.join(params).strip() == '':
	if origin.count('|') != 0: newo=origin[origin.find('|')+1:]
	elif origin.count('[') != 0: newo=origin[origin.find('[')+1:origin.find(']')]
	if newo.strip() != '': params=[newo]
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
			if params.count(' ') == 0: tclv=closest([params,params+' StateZ'],[team1,team2])
			else: tclv=closest([params,params.replace('st','state')],[team1,team2,team1+team2,team2+team1])
			if tclv < closestval:
				closestval=tclv
				closests=a
	if dest=='footballbot' or dest=='footballtestbot': dest=origin
	if closests != '' and closestval <= 2:
		ourgame=teams[closests]
		cis=artolower(db['colors'])
		if ourgame['team1'].lower() in cis: t1=chr(3)+str(cis[ourgame['team1'].lower()][0])+','+str(cis[ourgame['team1'].lower()][1])+ourgame['team1']
		else: t1=ourgame['team1']
		if ourgame['team2'].lower() in cis: t2=chr(3)+str(cis[ourgame['team2'].lower()][0])+','+str(cis[ourgame['team2'].lower()][1])+ourgame['team2']
		else: t2=ourgame['team2']
		t1=t1+' '+ourgame['team1score']
		t2=t2+' '+ourgame['team2score']
		if t1.count(chr(3)) != 0: t1+=chr(3)
		if t2.count(chr(3)) != 0: t2+=chr(3)
		tmtype='PRIVMSG'
		stsm=splitMessage(stats(ourgame['gid']))
		for sts in stsm:
			db['msgqueue'].append([origin+': '+t1+'-'+t2+' '+sts,dest,tmtype,'score'])
	else: db['msgqueue'].append([origin+': Could not find a match for this week...',dest,'PRIVMSG',None])
	#[msg,channel (all main chans), type(privmsg),identifier(None)]
=======


def sMsg(msg, l=400, split=','):
    if msg > l:
        msgs = []
        while len(msg) > l:
            msg1 = msg[:l][::-1]
            loc = len(msg1) - msg1.find(',')
            msgs.append(msg[:loc].strip())
            msg = msg[loc:].strip()
        if len(msg.strip()) > 0: msgs.append(msg.strip())
        return msgs
    else:
        return [msg]


def abbrev(words, abb, debug=False):
    con = abb
    print words
    for throw, ws in con.iteritems():
        #print words.lower()+'.'+ws[0].lower()+'.'
        if ws[0] != None and words.lower().strip() == ws[0].lower().strip():
            words = ws[1]
        #if debug: print words+'.'+ws[0]+'.'+ws[1]+'.'
    return words


if (origin.count('|') != 0 or origin.count('[') != 0
   ) and ''.join(params).strip() == '':
    if origin.count('|') != 0: newo = origin[origin.find('|') + 1:]
    elif origin.count('[') != 0:
        newo = origin[origin.find('[') + 1:origin.find(']')]
    if newo.strip() != '': params = [newo]
if ''.join(params).strip() != '':
    tbyname = {}
    closestval = 1000000
    closests = ''
    teams = db['games']
    params = abbrev(' '.join(params).lower(), db['abbreviations'])
    for a, b in teams.iteritems():
        if a != 'lastupdate':
            team1 = b['team1'].lower().replace('(', '').replace(')', '')
            team2 = b['team2'].lower().replace('(', '').replace(')', '')
            if params.count(' ') == 0:
                tclv = closest([params, params + ' StateZ'], [team1, team2])
            else:
                tclv = closest([params, params.replace('st', 'state')],
                               [team1, team2, team1 + team2, team2 + team1])
            if tclv < closestval:
                closestval = tclv
                closests = a
    if dest == 'footballbot' or dest == 'footballtestbot': dest = origin
    if closests != '' and closestval <= 2:
        ourgame = teams[closests]
        cis = artolower(db['colors'])
        if ourgame['team1'].lower() in cis:
            t1 = chr(3) + str(cis[ourgame['team1'].lower()][0]) + ',' + str(
                cis[ourgame['team1'].lower()][1]) + ourgame['team1']
        else:
            t1 = ourgame['team1']
        if ourgame['team2'].lower() in cis:
            t2 = chr(3) + str(cis[ourgame['team2'].lower()][0]) + ',' + str(
                cis[ourgame['team2'].lower()][1]) + ourgame['team2']
        else:
            t2 = ourgame['team2']
        t1 = t1 + ' ' + ourgame['team1score']
        t2 = t2 + ' ' + ourgame['team2score']
        if t1.count(chr(3)) != 0: t1 += chr(3)
        if t2.count(chr(3)) != 0: t2 += chr(3)
        tmtype = 'PRIVMSG'
        stsm = sMsg(stats(ourgame['gid']))
        for sts in stsm:
            db['msgqueue'].append([origin + ': ' + t1 + '-' + t2 + ' ' + sts,
                                   dest, tmtype, 'score'])
    else:
        db['msgqueue'].append(
            [origin + ': Could not find a match for this week...', dest,
             'PRIVMSG', None])
    #[msg,channel (all main chans), type(privmsg),identifier(None)]
>>>>>>> origin/master
