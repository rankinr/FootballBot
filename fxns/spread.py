"""
Returns betting info by team name.
"!spread" can be replaced with "$" (i.e., "$UMiami" will produce the same result as "!spread UMiami")
"""
db['spread']=json.loads(sql.unique_get('data','spread'))
if len(' '.join(params)) != ' '.join(params).count('!'):
	def abbrev(words,abb,debug=False):
		con=abb
		for throw,ws in con.iteritems():
			#print words.lower()+'.'+ws[0].lower()+'.'
			if ws[0] != None and words.lower().strip()==ws[0].lower().strip(): words=ws[1]
			#if debug: print words+'.'+ws[0]+'.'+ws[1]+'.'
		return words
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
			tmtype='PRIVMSG'
			neutral=True
			nident=''
			if 'neutral' in db['games'][closests]:
				neutral=db['games'][closests]['neutral']
			if not neutral: nident='@ '
			if closests in db['spread'] and closests in db['games']:
				spdisp=db['spread'][closests].strip()
				spdisp2=spdisp[spdisp.find(' ')+1:]
				spdisp2=spdisp2[spdisp2.find(' ')+1:].strip()
				sptext=''
				if spdisp.count('+') == 1 and spdisp.count('-') == 1:
					nitext=''
					if spdisp[0]=='-': 
						if nident=='@ ': nitext='playing at'
						else: nitext='over'
						spval=spdisp[1:spdisp.find(' ')]
						sptext=origin+': '+db['games'][closests]['team1']+' is favored by '+spval+' points '+nitext+' '+db['games'][closests]['team2']+' ('+spdisp2+')'
					elif spdisp[0]=='+': 
						if nident=='@ ': nitext='in its home game against'
						else: nitext='over'
						spval=spdisp[1:spdisp.find(' ')]
						sptext=origin+': '+db['games'][closests]['team2']+' is favored by '+spval+' points '+nitext+' '+db['games'][closests]['team1']+' ('+spdisp2+')'
				if sptext=='': sptext=origin+': '+db['games'][closests]['team1']+' '+nident+db['games'][closests]['team2']+' '+spdisp+chr(3)
				db['msgqueue'].append([sptext,dest,tmtype,'score'])
		else: db['msgqueue'].append([origin+': Could not find a match for this week.',dest,'PRIVMSG',None])
		#[msg,channel (all main chans), type(privmsg),identifier(None)]
