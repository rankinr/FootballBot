irc_flairs=json.loads("""{"North Dakota": "52,54", "Kentucky": "51,66", "Floridaa": "51,79", "Brown": "52,81", "Arizona": "51,47", "Duke": "51,04", "Columbia": "52,82", "Harvard": "52,85", "Penn State": "51,40", "Massachusetts": "52,23", "Jackson State": "53,69", "Clemson": "51,03", "Buffalo": "52,15", "TCU": "51,23", "UC Davis": "52,60", "Wake Forest": "51,15", "Georgia": "51,65", "Tulsa": "51,93", "RCFB": "51,01", "Houstona": "51,96", "Lehigh": "53,32", "Mercer": "53,47", "Tennessee": "51,72", "Syracuse": "51,12", "Mississippi Valley State": "53,70", "Iowa": "51,32", "Illinois": "51,30", "Texas Techa": "51,28", "Northwestern": "51,38", "Middle Tennessee": "52,03", "South Alabama": "52,45", "UCFa": "51,97", "Rhode Island": "52,75", "Northern Illinoisa": "52,25", "Wisconsin": "51,43", "West Virginia": "51,26", "Northern Iowa": "53,04", "UTEP": "52,09", "Louisiana Lafayette": "52,43", "Monmouth": "52,67", "Sacramento State": "52,58", "Notre Dame": "51,83", "Delaware State": "52,90", "Southern Illinois": "53,07", "Texas State": "52,46", "Appalachian State": "52,38", "Colgate": "53,27", "Northern Illinois": "52,20", "Ohio Statea": "51,46", "Temple": "51,91", "Houston": "51,87", "Charlotte": "51,98", "Virginia": "51,13", "Michigana": "51,45", "Mississippi State": "51,68", "Illinois State": "53,00", "Kansas State": "51,20", "Florida State": "51,05", "Nicholls State": "53,59", "Oklahoma": "51,21", "Cal Poly": "52,49", "South Dakota": "53,05", "Oklahoma State": "51,22", "Tulane": "51,92", "Texas Tech": "51,25", "Sam Houston State": "53,61", "Southeastern Louisiana": "53,62", "Liberty": "52,66", "Iowa State": "51,18", "Washington State": "51,58", "Idaho State": "52,51", "Wofford": "53,52", "Eastern Kentucky": "53,19", "Southern Mississippi": "52,07", "New Mexico State": "52,44", "SMU": "51,90", "Robert Morris": "53,13", "San Diego State": "52,33", "Grambling State": "53,68", "Delaware": "52,70", "Southern Utah": "52,59", "Bowling Green": "52,14", "Washington": "51,57", "Bucknell": "53,26", "Michigan State": "51,35", "Princeton": "52,87", "Weber State": "52,61", "Houston Baptist": "53,55", "Ohio State": "51,39", "Army": "51,81", "San Diego": "53,41", "Toledo": "52,22", "Ohio": "52,21", "Kennesaw State": "52,65", "Auburn": "51,63", "Texas San Antonio": "52,10", "Old Dominion": "52,05", "Florida A&M": "52,91", "NC State": "51,10", "Oregona": "51,59", "South Carolina State": "52,99", "Missouri": "51,69", "Nebraska": "51,37", "Howard": "52,93", "Texas Southern": "53,73", "Northwestern State": "53,60", "Memphis": "51,88", "Elon": "52,71", "Villanova": "52,79", "Ball State": "52,13", "Missouri State": "53,02", "Louisiana Tech": "52,01", "BYU": "51,82", "Western Michigan": "52,24", "Wagner": "53,16", "Rice": "52,06", "Cincinnati": "51,84", "Savannah State": "52,98", "Dayton": "53,36", "Albany": "52,69", "Youngstown State": "53,09", "Lafayette": "53,31", "Eastern Illinois": "53,18", "Stony Brook": "52,77", "McNeese State": "53,58", "Colorado State": "52,28", "Incarnate Word": "53,56", "Murray State": "53,21", "UCF": "51,94", "Akron": "52,12", "USC": "51,55", "East Carolina": "51,86", "Norfolk State": "52,95", "Marshall": "52,02", "Ole Missa": "51,77", "Miami (OH)": "52,19", "Maryland": "51,33", "Georgetown": "53,29", "William & Mary": "52,80", "Prairie View A&M": "53,71", "Boston College": "51,02", "Abilene Christian": "53,53", "FIU": "52,00", "East Tennessee State": "53,45", "Idaho": "52,42", "Dartmouth": "52,84", "Georgia Tech": "51,06", "Baylor": "51,17", "Minnesota": "51,36", "Campbell": "53,34", "Florida": "51,64", "Southern University": "53,72", "VMI": "53,50", "Northern Colorado": "52,56", "Richmond": "52,76", "California": "51,49", "South Florida": "51,95", "Arkansas State": "52,39", "Portland State": "52,57", "Samford": "53,48", "Utah": "51,56", "Stetson": "53,42", "Chattanooga": "53,44", "Arkansas-Pine Bluff": "53,67", "Fordham": "53,28", "Morgan State": "52,94", "Butler": "53,33", "Kansas": "51,19", "Indiana": "51,31", "UAB": "52,08", "New Hampshire": "52,74", "Southeast Missouri": "53,22", "Kentuckya": "51,76", "Colorado": "51,50", "Alabama A&M": "53,64", "Davidson": "53,35", "Fresno State": "52,29", "Western Carolina": "53,51", "Gardner-Webb": "52,64", "Coastal Carolina": "52,63", "Jacksonville": "53,38", "Alabama": "51,61", "Towson": "52,78", "Bethune-Cookman": "52,89", "Alabama State": "53,65", "North Texas": "52,04", "Tennessee-Martin": "53,25", "Nevada": "52,31", "Vanderbilt": "51,74", "Jacksonville State": "53,20", "Valparaiso": "53,43", "Navy": "51,89", "South Carolina": "51,71", "South Dakota State": "53,06", "San Jos\u00c3\u00a9 State": "52,34", "Hampton": "52,92", "Montana State": "52,53", "Sacred Heart": "53,14", "Arizona State": "51,48", "Drake": "53,37", "Central Arkansas": "53,54", "UNLV": "52,35", "Furman": "53,46", "St. Francis": "53,15", "Utah State": "52,36", "Texasa": "51,29", "Hawaii": "52,30", "Ole Miss": "51,70", "Charleston Southern": "52,62", "Pennsylvania": "52,86", "Pittsburgh": "51,11", "LSU": "51,67", "Texas A&M": "51,73", "Purdue": "51,41", "Stanforda": "51,60", "UCLA": "51,54", "Michigan": "51,34", "Yale": "52,88", "Duquesne": "53,12", "Boise State": "52,27", "Maine": "52,73", "Western Kentucky": "52,11", "Arkansas": "51,62", "North Carolina Central": "52,97", "Oregon State": "51,52", "Texas": "51,24", "Holy Cross": "53,30", "Northern Arizona": "52,55", "Oregon": "51,51", "Stanford": "51,53", "Alcorn State": "53,66", "Morehead State": "53,40", "Miami (FL)": "51,08", "Indianaa": "51,44", "Stephen F Austin": "53,63", "Troy": "52,47", "Tennessee Tech": "53,24", "Montana": "52,52", "Central Michigan": "52,16", "North Carolina": "51,09", "Texas A&Ma": "51,78", "North Carolina A&T": "52,96", "Central Connecticut": "53,11", "The Citadel": "53,49", "Alabamaa": "51,80", "Rutgers": "51,42", "FAU": "51,99", "Eastern Washington": "52,50", "Austin Peay": "53,17", "Kent State": "52,18", "Florida Statea": "51,16", "James Madison": "52,72", "Georgia State": "52,41", "Air Force": "52,26", "Presbyterian College": "52,68", "Connecticut": "51,85", "Tennessee State": "53,23", "Marist": "53,39", "Wyoming": "52,37", "Bryant": "53,10", "Eastern Michigan": "52,17", "New Mexico": "52,32", "North Dakota State": "53,03", "Virginia Tech": "51,14", "Indiana State": "53,01", "Georgia Southern": "52,40", "Western Illinois": "53,08", "ULM": "52,48", "Lamar": "53,57", "Cornell": "52,83", "Louisville": "51,07"}""")
#irc_flairs_new=json.loads(urllib.urlopen('http://162.243.6.111:7778/kiwi/assets/libs/final.json').read())
def shorten_url(url): # returns shortened URL
	try:
		post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyBZ3umk6db7MgXZbBsDZbZJDzFyx1ZVoH0'
		postdata = {'longUrl':url}
		headers = {'Content-Type':'application/json'}
		req = urllib2.Request(
			post_url,
			json.dumps(postdata),
			headers
		)
		ret = urllib2.urlopen(req).read()
		print ret
		return json.loads(ret)['id']
	except:
		return ''
def auth(username,lne):
	global just_authed
	global commands_pending_auth
	if username in just_authed: return True
	else:
		if not username in commands_pending_auth: commands_pending_auth[username]=[]
		commands_pending_auth[username].append(lne)
		db['msgqueue'].append(['ACC '+username,'NICKSERV'])
		return False
def keywords(line,keywords):
	all=True
	line=line.lower()
	for keyword in keywords:
		if line.count(keyword.lower()) == 0:
			all=False
	return all
def remove_text(line,torem):
	line=line.lower()
	for rem in torem:
		line=line.replace(rem.lower(),'  ')
	while line.count('  ') != 0: line=line.replace('  ',' ')
	return line.strip()
def count_numbers(ds):
	if re.search('[0-9]+', ds) != None:
		return len( (re.search('[0-9]+', ds)).group() )
	else:
		return 0
		
def splitMessage(original_message,l=400,split=','): #splits message into chucnks of maximum length l, separated my most recent character split before length l is reached
	#print original_message
	print len(original_message)
	if len(original_message) > l:
		new_message=''
		original_message=original_message.split(split)
		messages_to_send=[]
		c=0
		while len(split.join(original_message)) > l and c < 5:
			c+=1
			#print ('loop'+str(c))
			while len(new_message) < l and len(original_message) > 0:
				last_original_message_array=original_message[:]
				add_to_message=original_message.pop(0)
				last_original_message=new_message
				new_message+=add_to_message+split
			if len(messages_to_send) > 0: last_original_message="(cont'd) "+last_original_message.strip()
			messages_to_send.append(last_original_message.strip())
			original_message=last_original_message_array
			new_message=''
		if len(split.join(original_message).strip()) != 0:
			messages_to_send.append("(cont'd) "+split.join(original_message).strip())
		return messages_to_send
	else:
		return [original_message]

def most_recent_play(gid):
	pg=urllib.urlopen("http://espn.go.com/ncf/playbyplay?gameId="+gid).read()
	pg=pg[pg.find('var gamePackageData = ')+len('var gamePackageData = '):]
	pg=pg[:pg.find('}};')+2]
	try:
		pg=json.loads(pg)
		poss=k4v(str(pg['drives']['current']['plays'][0]['end']['team']['id']),db['teams'])
		toret=pg['drives']['current']['plays'][-1]['text']+', '+pg['drives']['current']['plays'][0]['end']['downDistanceText']+' (This drive: '+pg['drives']['current']['description']+')'
		return [toret,poss]
	except:
		return ['','']

def gameInfo(gm,color=False,showMr=False,score=True,branked=False,custformat='',supershort=False,newdb=False,typ_of_text='',showStatus=True,ircFlair=False):
	global irc_flairs_new
	for l_type in db['games_new']:
		if l_type != 'lastupdate' and gm in db['games_new'][l_type]: ourgame=db['games_new'][l_type][gm]
	if ourgame:
		if ourgame['status'].lower().count('pm et') != 0 or ourgame['status'].lower().count('am et') != 0: score=False
		t1c=''
		t2c=''
		if color:
			cis=artolower(db['colors'])
			if ourgame['team1'].lower() in cis:
				t1c1=str(cis[ourgame['team1'].lower()][0])
				t1c2=str(cis[ourgame['team1'].lower()][1])
				if len(t1c1) == 1: t1c1='0'+t1c1
				if len(t1c2) == 1: t1c2='0'+t1c2
				t1c=t1c1+','+t1c2
			if ourgame['team2'].lower() in cis: 
				t2c1=str(cis[ourgame['team2'].lower()][0])
				t2c2=str(cis[ourgame['team2'].lower()][1])
				if len(t2c1) == 1: t2c1='0'+t2c1
				if len(t2c2) == 1: t2c2='0'+t2c2
				t2c=t2c1+','+t2c2
		t1f=''
		t2f=''
		for team_info in irc_flairs_new:
			if team_info[6]==ourgame['team1']: t1f=team_info[1] #implementation of flair for custom version of kiwi 
			elif team_info[6]==ourgame['team2']: t2f=team_info[1]
		t1s=ourgame['team1']
		t2s=ourgame['team2']
		t1so=t1s
		t2so=t2s
		if supershort:
			shorts=artolower(db['supershorten'])
			#print 'yes'
		else: shorts=artolower(db['shorten'])
		if t1s.lower() in shorts and shorts[t1s.lower()].strip() != '': t1s=shorts[t1s.lower()]
		if t2s.lower() in shorts and shorts[t2s.lower()].strip() != '': t2s=shorts[t2s.lower()]
		if score:
			t1=t1s+' '+ourgame['team1score']
			t2=t2s+' '+ourgame['team2score']
		else:
			t1=t1s
			t2=t2s
		if len(t1.split()) > 1:
			if t1.split()[1][0]=='(': t1=t1.split()[0]
		if len(t2.split()) > 1:
			if t2.split()[1][0]=='(': t2=t2.split()[0]
		rks=artolower(db['ranks'])
		btgame=False
	#	print ourgame['team1'].lower()
		if ourgame['team1'].lower() in rks and rks[ourgame['team1'].lower()] != None and int(rks[ourgame['team1'].lower()]) <= 25:
			t1='('+rks[ourgame['team1'].lower()]+') '+t1
			#print branked
			if branked: btgame=True
		if ourgame['team2'].lower() in rks and rks[ourgame['team2'].lower()] != None and int(rks[ourgame['team2'].lower()]) <= 25:
			t2='('+rks[ourgame['team2'].lower()]+') '+t2
			if branked: btgame=True
		#print btgame
		ntwks=''
		if 'network' in ourgame and ourgame['network'] != '': ntwks=' - '+ourgame['network']
		#if gm in db['ntwks']:
		#	if db['ntwks'][gm] != '': ntwks=' - '+db['ntwks'][gm]
		mr=''
		if ourgame['status'].upper().count('FINAL') == 1: ntwks=''
		status=ourgame['status']
		if status.lower().count('am et') != 0 or status.lower().count('pm et') != 0:
			std=status
			stds=std[:std.find(',')]
			std=std[std.find(',')+2:]
			std=std[std.find(' ')+1:]
			std=std[std.find(' ')+1:]
			std=stds+' '+std
			status=std
		status=status.replace(' EST','')+ntwks
		poss=''
		if ourgame['status'].upper().count('FINAL') == 0 and ourgame['status'].upper().count('PM ET') == 0 and ourgame['status'].upper().count('AM ET') == 0 and showMr:
			mrg=ourgame['most_recent_play']
			poss=ourgame['possession']
			if showMr: mr=': '+mrg
			if len(mr) < 5: mr=''
			#if 'downDistanceText' in event['competitions'][0]['situation']['lastPlay']: mr+=', '+event['competitions'][0]['situation']['lastPlay']['downDistanceText']
		if ourgame['team1']==poss: t1=t1+' (:)'
		elif ourgame['team2']==poss: t2=t2+' (:)'
		if t1c != '': t1=chr(3)+t1c+t1+chr(3)
		if t2c != '': t2=chr(3)+t2c+t2+chr(3)
		if t1f != '': t1='*'+chr(3)+t1f[0]+chr(3)+t1f[1]+chr(3)+t1f[2]+chr(3)+t1f[3]+chr(3)+'*'+t1
		if t2f != '': t2='*'+chr(3)+t2f[0]+chr(3)+t2f[1]+chr(3)+t2f[2]+chr(3)+t2f[3]+chr(3)+'*'+t2
		nident=' vs. '
		if 'neutral' in ourgame and not ourgame['neutral']: nident=' @ '
		bt=''
		if btgame: bt='\x02'
		stat_to_show=ourgame['status'].strip()
		#if supershort and (stat_to_show.count('PM ET') != 0 or stat_to_show.count('AM ET') != 0):
		#	stat_to_show1=stat_to_show[:stat_to_show.find(',')].strip()
		#	stat_to_show2=stat_to_show[stat_to_show.find(',')+1:].strip()
		#	stat_to_show2=stat_to_show2[stat_to_show2.find(' '):].strip()
		#	stat_to_show2=stat_to_show2[stat_to_show2.find(' '):].strip()
		#	stat_to_show=stat_to_show1+' '+stat_to_show2
		if supershort: stat_to_show=stat_to_show.replace(' - ',' ')
		if not showStatus: stat_to_show=''
		if custformat != '':	
			return custformat.replace('%BT%',bt.strip()).replace('%T1%',t1.strip()).replace('%T2%',t2.strip()).replace('%NIDENT%',nident.strip()).replace('%MR%',mr.strip()).replace('%STATUS%',stat_to_show.strip()).replace('%NTWKS%',ntwks.strip())
		else:
			if stat_to_show != '': toretbase=t1.strip()+nident+t2.strip()+mr.strip()+' '+stat_to_show+' '+ntwks.strip()
			else: toretbase=t1.strip()+nident+t2.strip()+mr.strip()+' '+ntwks.strip()
			if typ_of_text=='time': toretbase=(stat_to_show+' - '+toretbase.replace(stat_to_show,'')).replace('  ',' ')
			elif typ_of_text=='channel' and ntwks.strip() != '': toretbase=(ntwks.replace('-','').strip()+' - '+toretbase.replace(ntwks.strip(),'')).replace('  ',' ')
			toretbase=toretbase.strip()
			return bt+toretbase+bt
	#			db['msgqueue'].append([t1+' '+nident+t2.strip()+mr.strip()+' '+ourgame['status']+ntwks,dest,tmtype,'score'])
	else: return 'Could not find match.'+gm

	
def gameMatch(params):
	tbyname={}
	closestval=1000000
	closests=''
	teams=db['games_new']['fbs'].copy()
	for l_type in db['games_new']:
		if l_type != 'lastupdate' and l_type != 'fbs': teams.update(db['games_new'][l_type])
	#print '1:'+params
	params_orig=params
	#print '2:'+params_orig
	if not params in team_list: params=abbrev(params,db['abbreviations'])
	#print '3:'+params
	#print '4:'+params_orig
	for a,b in teams.iteritems():
		if a != 'lastupdate' and closests != 0:
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
	bye=False
	if closestval != 0 and params_orig in team_list:
		bye=True
		params=params_orig
		closest_bye_alt=''
		if closestval <= 3: closest_bye_alt=closests
		closests=''
	if bye: return 'bye'
	else:
		if closests=='': return False
		else: return {'match':closests,'dist':closestval}
def cashVal(csh):
	toret=str(csh)
	if len(toret)-toret.find('.') ==2: toret=toret+'0'
	return toret
def getGameInfo(typ,league=False): # retrieves game information from espn scoreboard (typ = 80 is fbs teams, typ = 81 is fcs teams)
	if not league: urltoload='http://espn.go.com/college-football/scoreboard/_/group/'+typ+'/year/2015/seasontype/2/?t='+str(time.time())
	else: urltoload=league
	scoreboard=urllib.urlopen(urltoload).read()
	scoreboard=scoreboard[scoreboard.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):]
	scoreboard=json.loads(scoreboard[:scoreboard.find('}};')+2])
	games={}
	for event in scoreboard['events']:
		this_game={}
		if not league or typ=='bowl':
			this_game['team2']=event['competitions'][0]['competitors'][0]['team']['location']
			this_game['team1']=event['competitions'][0]['competitors'][1]['team']['location']
		else:
			this_game['team2']=event['competitions'][0]['competitors'][0]['team']['shortDisplayName']
			this_game['team1']=event['competitions'][0]['competitors'][1]['team']['shortDisplayName']
		this_game['team2abbreviation']=event['competitions'][0]['competitors'][0]['team']['abbreviation']
		this_game['team1abbreviation']=event['competitions'][0]['competitors'][1]['team']['abbreviation']
		this_game['team2score']=event['competitions'][0]['competitors'][0]['score']
		this_game['team1score']=event['competitions'][0]['competitors'][1]['score']
		if 'odds' in event['competitions'][0] and len(event['competitions'][0]) > 0 and 'details' in event['competitions'][0]['odds'][0] and 'overUnder' in event['competitions'][0]['odds'][0]:
			this_game['odds']=event['competitions'][0]['odds'][0]['details']+' '+str(event['competitions'][0]['odds'][0]['overUnder'])+' O/U'+' ('+event['competitions'][0]['odds'][0]['provider']['name']+')'
		most_recent_play=''
		this_game['possession']=None
		if event['competitions'][0] != None and 'situation' in event['competitions'][0] and event['competitions'][0]['situation'] != None and  'lastPlay' in event['competitions'][0]['situation'] and event['competitions'][0]['situation']['lastPlay'] != None and 'text' in event['competitions'][0]['situation']['lastPlay']:
			most_recent_play=event['competitions'][0]['situation']['lastPlay']['text']
			if most_recent_play[0]=='(':
				most_recent_play=most_recent_play[1:]
				if most_recent_play[-1]==')': most_recent_play=most_recent_play[:-1]
			if 'downDistanceText' in event['competitions'][0]['situation']:
				most_recent_play=most_recent_play+', '+event['competitions'][0]['situation']['downDistanceText']
			if 'drive' in  event['competitions'][0]['situation']['lastPlay'] and 'description' in event['competitions'][0]['situation']['lastPlay']['drive']:
				most_recent_play=most_recent_play+' (This drive: '+event['competitions'][0]['situation']['lastPlay']['drive']['description']+')'
			if 'possession' in event['competitions'][0]['situation']: 
				possr=event['competitions'][0]['situation']['possession']
				if possr.count('?') != 0: possr=possr[:possr.find('?')].strip()
				this_game['possession']=k4v(str(possr),db['teams'])
		this_game['most_recent_play']=most_recent_play
		hometeam=''
		this_game['neutral']=True
		if event['competitions'][0]['competitors'][0]['homeAway']=='home':
			this_game['hometeam']=this_game['team2']
			this_game['neutral']=False
		elif event['competitions'][0]['competitors'][1]['homeAway']=='home':
			hometeam=this_game['team1']
			this_game['neutral']=False
		this_game['gid']=event['id']
		this_game['temperature']=''
		this_game['location']=''
		if 'weather' in event:
			if 'temperature' in event['weather']: this_game['temperature']=str(event['weather']['temperature'])+'F'
			elif 'highTemperature' in event['weather']: this_game['temperature']=str(event['weather']['highTemperature'])+'F'
			if 'conditions' in event['weather']: 
				condns=event['weather']['conditions']
				condns=condns[0].upper()+condns[1:]
				this_game['temperature']=(condns+' '+this_game['temperature']).strip()
		if 'venue' in event['competitions'][0] and 'fullName' in event['competitions'][0]['venue']: this_game['location']=event['competitions'][0]['venue']['fullName']
		this_game['status']=event['status']['type']['shortDetail'].replace('EST','EDT').replace('EDT','ET')
		if 'broadcasts' in event['competitions'][0] and len(event['competitions'][0]['broadcasts']) > 0 and len(event['competitions'][0]['broadcasts'][0]['names']) > 0:
			this_game['network']=', '.join(event['competitions'][0]['broadcasts'][0]['names'])
		else: this_game['network']=''
		games[this_game['team1']+this_game['team2']]=this_game
	return games # team1, team1score, team2, team2score, hometeam, neutral, temperature, status

def abbrev(words,abb,debug=False):
	if words == None:
		return ''
	else:
		new_word=''
		con=abb
		closest_val=99
		for throw,ws in con.iteritems():
			#print words.lower()+'.'+ws[0].lower()+'.'
			if ws[0] != None:
				cur_d=lev(words.lower().strip(),ws[0].lower().strip())
				if cur_d <= 1 and cur_d < closest_val:
					new_word=ws[1]
					#print words+' '+ws[0]+' '+str(cur_d)+' '+str(closest_val)
					closest_val=cur_d
			#if debug: #print words+'.'+ws[0]+'.'+ws[1]+'.'
		if new_word == '': new_word=words
		return new_word #add a space so it doesn't match perfectly, and if there is a more accurate matching team that will take precedent (so it says there is a bye week)

def stats(gid):
	try:
		soup=BeautifulSoup(urllib.urlopen('http://espn.go.com/college-football/matchup?gameId='+gid).read(),"html5lib")
		teams=soup.findAll('span',{'class':'chartLabel'})
		t1=teams[0].getText()
		t2=teams[1].getText()
		tb=soup.find('article',{'class':'team-stats-list'})
		tb=tb.find('table',{'class':'mod-data'})
		rows=tb.findAll('tr')
		stats=[]
		for row in rows:
			if row['class'][0]!='header':
				cols=row.findAll('td')
				if len(cols) > 2: stats.append(cols[0].contents[0].strip()+': '+t1+' '+cols[1].contents[0].strip()+' '+t2+' '+cols[2].contents[0].strip())
		return ', '.join(stats)
	except: return 'Oops! something went wrong.'

def k4v(v,ar): # return key for value v in array ar
	for a,b in ar.iteritems():
		if b == v:
			return a

def artolower(art): #make all values in array lowercase
	newar={}
	for a,b in art.iteritems(): newar[a.lower()]=b
	return newar
def lsttolower(art): #make all values in array lowercase
	newar=[]
	for a in art: newar.append(a.lower())
	return newar

def remove_rank(dstr): # removes ranking from team name
	return re.sub(r'\([0-9)]*\)', '',dstr).strip()
	
def match(w): # find closest team to w
	closestval=1000000
	closests=''
	teams=db['games_new']['fbs']
	params=abbrev(w.lower(),db['abbreviations'],True)
	for a,b in teams.iteritems():
		if a != 'lastupdate':
			team1=b['team1'].lower().replace('(','').replace(')','')
			team2=b['team2'].lower().replace('(','').replace(')','')
			tclv1=closest([params,params+' StateZ'],[team1])
			tclv2=closest([params,params+' StateZ'],[team2])
			if tclv1 < closestval:
				closestval=tclv1
				closests=team1
			if tclv2 < closestval:
				closestval=tclv2
				closests=team2
	if closests != '' and closestval < 3:
		return closests
	else:
		return False

def closest(one,two):
	lowest=1000
	for o in one:
		o=o.replace(')','').replace('(','').replace('  ',' ').lower().strip()
		for t in two:
			thisdist=lev(o,t.replace(')','').replace('(','').replace('  ',' ').lower().strip())
			if thisdist < lowest and (thisdist <=1 or (thisdist <=3 and len(t) > 5) or (thisdist <=5 and len(t) > 7)):
				lowest=thisdist
	return lowest
