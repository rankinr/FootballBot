<<<<<<< HEAD
time.sleep(1)
this_loop_start_time=time.time()

#LOAD DATABASE

if not sql.db.open or l_mysql_refresh < time.time()-3600:
	sql=mysql()
	l_mysql_refresh=time.time()
=======
if time.time() - this_loop > 1.1: print 'looplen' + str(time.time() - this_loop)
#print 'loop'
this_loop = time.time()
flood_control_channel = '#redditcfb'  #SET CHANNEL TO DO FLOOD CONTROL ON
flood_max_lag = 2
if not sql.db.open or l_mysql_refresh < time.time() - 3600:
    sql = mysql()
    l_mysql_refresh = time.time()
db['flood_kick'] = [[4, 5]]

##### SQL COMPATIBILITY VARIABLE SETTING
>>>>>>> origin/master

db['language'] = {}
if not 'msgqueue' in db: db['msgqueue'] = []

sql.cur.execute("""select * from data""")
a = sql.cur.fetchall()
for b in a:
<<<<<<< HEAD
	if b[0]=='drunklevel' or b[0] =='drunksetting':
		if b[0] == 'drunklevel': db[b[0]]=int(b[1])
		else: db[b[0]]=b[1]
	else:
		if b[0].count('language') == 0: db[b[0]]=json.loads(b[1])
		else:
			db['language'][b[0][b[0].find('language-')+len('language-'):]]=json.loads(b[1])
=======
    if b[0] == 'drunklevel' or b[0] == 'drunksetting':
        if b[0] == 'drunklevel': db[b[0]] = int(b[1])
        else: db[b[0]] = b[1]
    else:
        if b[0].count('language') == 0: db[b[0]] = json.loads(b[1])
        else:
            db['language'][b[0][b[0].find('language-') + len('language-'):]
                 ] = json.loads(b[1])
db['blockusers'] = []
>>>>>>> origin/master

if len(ns_ping) == 3: ns_ping = [0, 0, 20, 0]
if len(mostrecentnicks) > 10: mostrecentnicks = mostrecentnicks.pop(0)
#db['msgqueue']=[]
mostrecentnicks = []

<<<<<<< HEAD
if len(mostrecentnicks) > 10: mostrecentnicks=mostrecentnicks.pop(0)
#db['msgqueue']=[]
mostrecentnicks=[]
=======

>>>>>>> origin/master
#db['msgqueue']=[]
#abob_sent=False
def abbrev(words, abb, debug=False):
    con = abb
    for throw, ws in con.iteritems():
        #print words.lower()+'.'+ws[0].lower()+'.'
        if words.lower().strip() == ws[0].lower().strip(): words = ws[1]
        #if debug: #print words+'.'+ws[0]+'.'+ws[1]+'.'
    return words


for a, b in pastcmd.iteritems():
    for c in b:
        if c < time.time() - 60: b.pop(b.index(c))
if time.localtime()[3] == 5:
<<<<<<< HEAD
	sql.unique_set('data','drunklevel',str(0))
	cursedHoya=False
	pastcmd={}
dlevel=0
=======
    db['drunklevel'] = 0
    cursedHoya = False
    pastcmd = {}
dlevel = 0
>>>>>>> origin/master
#db['drunksettings']['active']=False
if db['drunksettings']['active']: dlevel = db['drunklevel']
#db['drunkmanual']='10' #drunksetting=manual, formula; drunkformula; #drunkmanual
#if drunksetting=='manual':#
#	dlevel=
#elif drunksetting=='formula':
#	dlevel=eval(db['drunkformula'].replace('x',str(db['drunklevel'])).replace("^","**"       )
#else:
#	dlevel=0
#dlevel=(math.log(float(db['drunklevel']+50)/float(7))*.07-.138)
#dlevel=math.pow(1.5,(math.log(float(db['drunklevel']+50))))
#dlevel=round(db['drunklevel']/100,0)
#if dlevel < 0: dlevel=0
lasterr = ''
"""if dlevel > 10 and cursedHoya==False:
	msg=random.choice(['Holy fuck,','Motherfucking','Holy Shit','For fucks sake','FUCKKK!','Fucksticks','It\'s just fuck'])
	msg+=' Hoya14[Bama]'+'!'*random.randrange(1,40)
	cursedHoya=True
	db['msgqueue'].append([msg,"#redditcfb"])
"""
<<<<<<< HEAD
for a,b in db['games'].iteritems():
	if a != 'lastupdate':
		if (b['status'].count(' AM') != 0 or b['status'].count(' PM') != 0):
			if not b['gid'] in announced:
				year=time.strftime('%Y')
				tstart=time.strptime(b['status'].replace(' ET',' ')+year,"%a, %b %d %I:%M %p %Y")
				if tstart < time.time()-3600*30*24: tstart=time.strptime(b['status'].replace(' ET',' ')+str(int(year)+1),"%a, %b %d %I:%M %p %Y")
				tstart=time.mktime(tstart)
				if tstart < time.time()+60*5:
					announced.append(b['gid'])
					db['msgqueue'].append([b['team1']+' @ '+b['team2']+' starts in 5 minutes.','#redditcfb',None,None])
#announced=[]
=======
toaddlog = []
upcg = []
for b, a in db['games'].iteritems():
    if b != 'lastupdate':
        st = str(a['status']).lower()
        yr = time.strftime('%Y')
        #if st.count('jan') != 0: yr=str(int(yr)+1)
        #		print st
        if st.count('pm et') != 0 or st.count('am et') != 0:
            stp = st.replace(' et', '')
            stp = time.mktime(time.strptime(stp + ' ' + yr,
                                            '%a, %b %d %I:%M %p %Y'))
            #print stp-time.time()
"""			if stp < time.time()+100 and not a['team1']+a['team2']+str(stp) in db['old_ann_upcoming']:
				mx=' vs. '
				if 'neutral' in a and not a['neutral']: mx=' @ '
				upcg.append([a['team1']+mx+a['team2'],a['gid'],b])
				db['old_ann_upcoming'].append(a['team1']+a['team2']+str(stp))
"""
>>>>>>> origin/master
if chansold != db['config']['chans']:
    chansold = db['config']['chans']
    chanlist = []
    for ctype, chans in db['config']['chans'].iteritems():
        for c in chans:
            if chanlist.count(chans) == 0: chanlist.append(c)
    for chan in chanlist:
        s.send('join %s\r\n' % chan)
        time.sleep(1)
        open('logs/interact.log', 'a').write(time.strftime('%a %b %d %H:%M') +
                                             ": I joined " + chan + "\r\n")
        open('logs/interactw.log', 'a').write(time.strftime('%a %b %d %H:%M') +
                                              ": I joined " + chan + "\r\n")
try:
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()
    for line in temp:
        line = string.rstrip(line)
        #print line
        line = string.split(line)
        lines.append(line)
        #print line
except:
    nodata = 1
astrobob = False
for line in lines:
<<<<<<< HEAD
	tlana=' '.join(line)
	print tlana
	
	#CHECK FOR NICKSERV PING REPLY###
	
	#:nickserv!nickserv@services. notice footballbot :harkatmuld acc 1
	if ((tlana.lower().count('footballbot') != 0 or tlana.count('harkat') != 0 or tlana.count(' bot ') != 0)) and tlana.count('freenode.net') == 0 and tlana.count('PING') == 0:
		origin=line[0][1:line[0].find('!')]
		if origin.lower() != 'footballbot' and origin.lower() != 'harkatmuld': db['msgqueue'].append([tlana,'harkatmuld',None,None,False])
		if origin.lower().count('astrobob') != 0: astrobob=True
	if line[0].lower()=="ping":
		s.send("PONG %s\r\n" % line[1])
		#print "PONG %s\r\n" % line[1]
		#open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': PING PONG\r\n')
	elif line[1].lower() == 'join':
		origin=line[0][1:line[0].find('!')]
		channel_join=line[-1]
		#print 'user:'+origin+'.channel:'+channel_join+'.'
	elif len(line) >3:
		origin=line[0][1:line[0].find('!')]
		dest=line[2]
		mostrecentnicks.append(origin)

		open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': '+origin+' to '+line[2]+': '+' '.join(line[3:])[1:]+'\r\n')
		open('logs/interactw.log','a').write(time.strftime('%a %b %d %H:%M')+': '+origin+' to '+line[2]+': '+' '.join(line[3:])[1:]+'\r\n')
		######################-TWITTER STATUS DISPLAY-####################
		turl=''
		if ' '.join(line).lower().count('reddit.com/') == 1 and ' '.join(line).lower().count('/comments/') != 0:
			dest=line[2]
			tl=' '.join(line)
			turl='http://www.'+tl[tl.find('reddit.com/'):]
			if turl.count(' ') != 0: turl=turl[:turl.find(' ')]
			if turl[-1] == '/': turl=turl[:-1]
			if len(turl[::-1][:turl[::-1].find('/')]) < 15:
				r = praw.Reddit('<USERAGENT>')
				comment = r.get_submission(turl).comments[0]
				if dest == 'footballbot': dest=origin
				#print comment.author
				db['msgqueue'].append([str(comment.author)+': '+comment.body[:400]+chr(3),dest,None,None,False])
		if ' '.join(line).count('twitter.com/') == 1 and (' '.join(line).count('/status/') == 1 or ' '.join(line).count('/statuses/') == 1) and (line[2]!='#redditcfb'):
			for a in line:
				if a.count('twitter.com') == 1:
					ts=''
					turl=a
					if a.count('statuses') == 1: ts='statuses'
					elif a.count('status') == 1: ts='status'
					#print ts
					#print a
					tid=a[a.find(ts)+len(ts)+1:]
					#if tid.count('/') != '': tid=tid[:tid.find('/')]
			dest=line[2]
			CONSUMER_KEY = ""
			CONSUMER_SECRET = ""
			ACCESS_KEY = ""
			ACCESS_SECRET = ""
			consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
			access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
			client = oauth.Client(consumer, access_token)
			#print tid
			timeline_endpoint = "https://api.twitter.com/1.1/statuses/show.json?id="+tid
			resp = client.request(timeline_endpoint)
			#print resp
			response=resp[0]
			data=resp[1]
			#print response
			tweets = json.loads(data)
			#print tweets
			#print tweets
			#print tid
			tweets['text']=tweets['text'].encode('ascii','ignore')
			tweets['text']=(u''+tweets['text']).decode('utf-8')
			txt=tweets['text'].replace('pic.twitter.com','https://pic.twitter.com')
			repto=''
			if 'in_reply_to_screen_name' in tweets:
				if tweets['in_reply_to_screen_name'] != None and len(tweets['in_reply_to_screen_name']) > 1: repto=(u''+tweets['in_reply_to_screen_name']).decode('utf-8')
			twiuser=turl[turl.find('twitter.com/')+len('twitter.com/'):]
			twiuser=twiuser[:twiuser.find('/')]
			if repto != '': repto=', replying to '+repto
			db['msgqueue'].append(['@'+twiuser+repto+': '+txt+chr(3),dest,None,None,False])
		##############
		ful=' '.join(line)
		if len(line[3]) > 2:
			if line[3][1] == '$' and line[3][2].isalpha(): line[3]=':!$'+line[3][2:]
			elif line[3][1] == '?' and line[3][2].isalpha():
				line=line[:3]+[':!info']+line[3:]
				if len(line) >= 4: line[4]=line[4][2:]
				#print line
				#				elif line[3][1] == '#' and line[3][2].isalpha():
#					line.append(line[3][2:])
#					line[3]=':!stats'
			#print pastcmd[origin]
			#print len(pastcmd[origin])
			allowit=True
			if origin in pastcmd:
				if len(pastcmd[origin]) > 4: allowit=False
			if line[3][1]=='!' and allowit:
				#print line
				#if origin.lower().count('ptyyy') != 0: dlevel=1000000
				if not origin in pastcmd: pastcmd[origin]=[]
				pastcmd[origin].append(time.time())
				if not 'fxnsdir' in cached:
					os.system('ls -lah /home/fbbot/cfb/fxns/ > .fxnsdir')
					cached['fxnsdir']=open('.fxnsdir').read()
					os.system('rm .fxnsdir')
				if cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py\n') == 0 and cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py ') == 0:
					line[3]=line[3][2:].lower()
					#db['msgqueue'].append([line[3][0],'harkatmuld'])
					if line[3][0] == '$':
						line=line[:3]+[':!spread']+line[3:]
						line[4]=line[4][1:]
					elif line[3][0] == '#':
						line=line[:3]+[':!twi']+line[3:]
						line[4]=line[4][1:]
					elif line[3][0] == '?': line=line[:3]+[':!info']+line[3:]
					else: line=line[:3]+[':!score']+line[3:]
					#print line
				if ' '.join(line[3:]).count('.') ==0 and ((cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py\n') != 0) or (cached['fxnsdir'].count(' '+line[3][2:].lower()+'.py ') != 0)):
					origin=line[0][1:line[0].find('!')]
					dest=line[2].lower()
					params=line[4:]
					params=' '.join(params).lower()
					params=params.replace('\n','').replace('\r','')
					params=params[:300]
					if len(params.strip()) == 0: params=[]
					else: params=params.split(' ')
					if not line[3][2:].lower()+'_ucmd' in cached: cached[line[3][2:].lower()+'_ucmd']=open('/home/fbbot/cfb/fxns/'+line[3][2:].lower()+'.py').read()
					exec cached[line[3][2:].lower()+'_ucmd']
			#db['msgqueue'].append(['test'+str(time.time())+line[3][2:]+str(' '.join(line).count('.')),'#cfbtest'])
#else: open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': '+' '.join(line)+'\r\n')
#print len(db['msgqueue'])
c=0
for a in db['msgqueue']:
	if a[0]==None: db['msgqueue'][c]=['Remove','#cfbtest']
	c+=1
=======
    tlana = ' '.join(line)
    print tlana
>>>>>>> origin/master

    #CHECK FOR NICKSERV PING REPLY###

    cts = str(round(ns_ping[0]))
    if cts.count('.') != 0: cts = cts[:cts.find('.')]
    if tlana.find(
            ':nickserv!nickserv@services. notice footballbot') == 0 and tlana.count(
                    ' acc 3') == 1:
        user_authed = tlana[tlana.find(
            ':nickserv!nickserv@services. notice footballbot') + len(
                ':nickserv!nickserv@services. notice footballbot :'):tlana.find(
                    ' acc 3')]
        if user_authed in db['join_act']:
            s.send(db['join_act'][user_authed]['action'] + '\r\n')
    #:nickserv!nickserv@services. notice footballbot :harkatmuld acc 1
    if ((tlana.lower().count('footballbot') != 0 or tlana.count('harkat') != 0
             or tlana.count(' bot ') != 0)
    ) and tlana.count('freenode.net') == 0 and tlana.count('PING') == 0:
        origin = line[0][1:line[0].find('!')]
        if origin.lower() != 'footballbot' and origin.lower() != 'harkatmuld':
            db['msgqueue'].append([tlana, 'harkatmuld', None, None, False])
        if origin.lower().count('astrobob') != 0: astrobob = True
    if line[0].lower() == "ping":
        s.send("PONG %s\r\n" % line[1])
        #print "PONG %s\r\n" % line[1]
        #open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': PING PONG\r\n')
    elif line[1].lower() == 'join':
        origin = line[0][1:line[0].find('!')]
        channel_join = line[-1]
        #print 'user:'+origin+'.channel:'+channel_join+'.'
        if origin in db['join_act'] and db['join_act'][origin]['channel'
                                                        ] == channel_join:
            db['msgqueue'].append(['acc ' + origin, 'nickserv', 'privmsg'])
    elif len(line) > 3:
        origin = line[0][1:line[0].find('!')]
        dest = line[2]
        if dest.lower() == flood_control_channel.lower():  # CHANNEL FOR FLOOD CONTROL
            if origin in msgs_flood:
                msgs_flood[origin].append(time.time())
            else:
                msgs_flood[origin] = [time.time()]
            last_loop = time.time()
            #flood_hosts[origin]=line[0][line[0].find('@')+1:].strip()
        mostrecentnicks.append(origin)
        #if origin in db['blockusers']: db['msgqueue'].append(['You have been blocked from using FootballBot. Contact harkatmuld with any questions.',origin,None,None,False])
        if not origin in db['blockusers']:
            open('logs/interact.log', 'a').write(
                time.strftime('%a %b %d %H:%M') + ': ' + origin + ' to ' +
                line[2] + ': ' + ' '.join(line[3:])[1:] + '\r\n')
            open('logs/interactw.log', 'a').write(
                time.strftime('%a %b %d %H:%M') + ': ' + origin + ' to ' +
                line[2] + ': ' + ' '.join(line[3:])[1:] + '\r\n')
            ######################-TWITTER STATUS DISPLAY-####################
            turl = ''
            if ' '.join(line).lower().count('reddit.com/') == 1 and ' '.join(
                    line).lower().count('/comments/') != 0:
                dest = line[2]
                tl = ' '.join(line)
                turl = 'http://www.' + tl[tl.find('reddit.com/'):]
                if turl.count(' ') != 0: turl = turl[:turl.find(' ')]
                if turl[-1] == '/': turl = turl[:-1]
                if len(turl[::-1][:turl[::-1].find('/')]) < 15:
                    r = praw.Reddit('<USERAGENT>')
                    comment = r.get_submission(turl).comments[0]
                    if dest == 'footballbot': dest = origin
                    #print comment.author
                    db['msgqueue'].append([str(
                        comment.author) + ': ' + comment.body[:400] + chr(3),
                                           dest, None, None, False])
            if ' '.join(line).count('twitter.com/') == 1 and (
                    ' '.join(line).count('/status/') == 1 or
                    ' '.join(line).count('/statuses/') == 1) and (
                            line[2] != '#redditcfb'):
                for a in line:
                    if a.count('twitter.com') == 1:
                        ts = ''
                        turl = a
                        if a.count('statuses') == 1: ts = 'statuses'
                        elif a.count('status') == 1: ts = 'status'
                        #print ts
                        #print a
                        tid = a[a.find(ts) + len(ts) + 1:]
                        #if tid.count('/') != '': tid=tid[:tid.find('/')]
                dest = line[2]
                CONSUMER_KEY = ""
                CONSUMER_SECRET = ""
                ACCESS_KEY = ""
                ACCESS_SECRET = ""
                consumer = oauth.Consumer(key=CONSUMER_KEY,
                                          secret=CONSUMER_SECRET)
                access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
                client = oauth.Client(consumer, access_token)
                #print tid
                timeline_endpoint = "https://api.twitter.com/1.1/statuses/show.json?id=" + tid
                resp = client.request(timeline_endpoint)
                #print resp
                response = resp[0]
                data = resp[1]
                #print response
                tweets = json.loads(data)
                #print tweets
                #print tweets
                #print tid
                tweets['text'] = tweets['text'].encode('ascii', 'ignore')
                tweets['text'] = (u'' + tweets['text']).decode('utf-8')
                txt = tweets['text'].replace('pic.twitter.com',
                                             'https://pic.twitter.com')
                repto = ''
                if 'in_reply_to_screen_name' in tweets:
                    if tweets['in_reply_to_screen_name'] != None and len(
                            tweets['in_reply_to_screen_name']) > 1:
                        repto = (
                            u'' + tweets['in_reply_to_screen_name']
                        ).decode('utf-8')
                twiuser = turl[turl.find('twitter.com/') + len('twitter.com/'):]
                twiuser = twiuser[:twiuser.find('/')]
                if repto != '': repto = ', replying to ' + repto
                db['msgqueue'].append(['@' + twiuser + repto + ': ' + txt + chr(
                    3), dest, None, None, False])
            ##############
            ful = ' '.join(line)
            if len(line[3]) > 2:
                if line[3][1] == '$' and line[3][2].isalpha():
                    line[3] = ':!$' + line[3][2:]
                elif line[3][1] == '?' and line[3][2].isalpha():
                    line = line[:3] + [':!info'] + line[3:]
                    if len(line) >= 4: line[4] = line[4][2:]
                    #print line
                    #				elif line[3][1] == '#' and line[3][2].isalpha():
                    #					line.append(line[3][2:])
                    #					line[3]=':!stats'
                    #print pastcmd[origin]
                    #print len(pastcmd[origin])
                allowit = True
                if origin in pastcmd:
                    if len(pastcmd[origin]) > 4: allowit = False
                if line[3][1] == '!' and allowit:
                    #print line
                    #if origin.lower().count('ptyyy') != 0: dlevel=1000000
                    if not origin in pastcmd: pastcmd[origin] = []
                    pastcmd[origin].append(time.time())
                    if not 'fxnsdir' in cached:
                        os.system('ls -lah /home/fbbot/cfb/fxns/ > .fxnsdir')
                        cached['fxnsdir'] = open('.fxnsdir').read()
                        os.system('rm .fxnsdir')
                    if cached['fxnsdir'].count(' ' + line[3][2:].lower(
                    ) + '.py\n') == 0 and cached['fxnsdir'].count(
                            ' ' + line[3][2:].lower() + '.py ') == 0:
                        line[3] = line[3][2:].lower()
                        #db['msgqueue'].append([line[3][0],'harkatmuld'])
                        if line[3][0] == '$':
                            line = line[:3] + [':!spread'] + line[3:]
                            line[4] = line[4][1:]
                        elif line[3][0] == '#':
                            line = line[:3] + [':!twi'] + line[3:]
                            line[4] = line[4][1:]
                        elif line[3][0] == '?':
                            line = line[:3] + [':!info'] + line[3:]
                        else:
                            line = line[:3] + [':!score'] + line[3:]
                        #print line
                    if ' '.join(line[3:]).count('.') == 0 and (
                        (cached['fxnsdir'].count(' ' + line[3][2:].lower(
                        ) + '.py\n') != 0) or (cached['fxnsdir'].count(
                                ' ' + line[3][2:].lower() + '.py ') != 0)):
                        origin = line[0][1:line[0].find('!')]
                        dest = line[2].lower()
                        params = line[4:]
                        params = ' '.join(params).lower()
                        params = params.replace('\n', '').replace('\r', '')
                        params = params[:300]
                        if len(params.strip()) == 0: params = []
                        else: params = params.split(' ')
                        if not line[3][2:].lower() + '_ucmd' in cached:
                            cached[line[3][2:].lower() + '_ucmd'] = open(
                                '/home/fbbot/cfb/fxns/' + line[3][2:].lower(
                                ) + '.py').read()
                        exec cached[line[3][2:].lower() + '_ucmd']
                #db['msgqueue'].append(['test'+str(time.time())+line[3][2:]+str(' '.join(line).count('.')),'#cfbtest'])
                #else: open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': '+' '.join(line)+'\r\n')
                #print len(db['msgqueue'])
c = 0
for a in db['msgqueue']:
    if a[0] == None: db['msgqueue'][c] = ['Remove', '#cfbtest']
    c += 1
"""
				#drunksettings ->
					curse
					names
					appendages
					toodrunk
					duplicate
					SUBS:
						randomize
						min
"""
"""db['drunksettings']={}
db['drunksettings']['curse']={}
db['drunksettings']['names']={}
db['drunksettings']['appendages']={}
db['drunksettings']['toodrunk']={}
db['drunksettings']['duplicate']={}

db['drunksettings']['curse']['randomize']=10000
db['drunksettings']['names']['randomize']=15000
db['drunksettings']['appendages']['randomize']=8000
db['drunksettings']['toodrunk']['randomize']=25000
db['drunksettings']['duplicate']['randomize']=5000

db['drunksettings']['curse']['min']=1500
db['drunksettings']['names']['min']=2000
db['drunksettings']['appendages']['min']=1750
db['drunksettings']['toodrunk']['min']=3500
db['drunksettings']['duplicate']['min']=380
db['drunksettings']['slur']={}
db['drunksettings']['insert']={}
db['drunksettings']['slur']['randomize']=100
db['drunksettings']['slur']['min']=100	
db['drunksettings']['insert']['randomize']=100
db['drunksettings']['insert']['min']=100	"""
<<<<<<< HEAD
if len(db['msgqueue']) != 0 and time.time() > lastsent+.3:
	sql.unique_set('data','drunklevel',str(int(db['drunklevel'])+1))
	#[msg,channel (all main db['config']['chans']), type(privmsg),identifier(None)]
	#print db['msgqueue']
	#print db['msgqueue'][0][0]
	db['msgqueue'][0][0]=db['msgqueue'][0][0].encode('ascii','ignore').replace('\r','').replace('\n','')
	if len(db['msgqueue'][0]) >=5: cursing=db['msgqueue'][0][4]
	else: cursing=True
	if len(db['msgqueue'][0])  >= 4: 
		midentifier=db['msgqueue'][0][3]
	else: midentifier=None
	if len(db['msgqueue'][0]) >=3:
		if db['msgqueue'][0][2] == None: mtype='PRIVMSG'
		else: mtype=db['msgqueue'][0][2]
	else: mtype='PRIVMSG'
	if len(db['msgqueue'][0]) >=2:
		if db['msgqueue'][0][1]==None: mchannel=db['config']['chans']
		else: mchannel=db['msgqueue'][0][1]
	else: mchannel=db['config']['chans']
	msg=db['msgqueue'][0][0][:550].replace('&nbsp;',' ')
	abob=''
	if astrobob: abob=chr(3)+'0,5'
	msg=msg.strip().replace('%ABOB%',abob)
	if abob != '': msg+=chr(3)
	#msg, mchannel, mtype, midentifier
	if (lastmsg != msg or time.time() > lastsent+3 or 1==1) and msg != '':
		if isinstance(mchannel,basestring): mchannel={'all':[mchannel]}
		elif isinstance(mchannel,list): mchannel={'all':mchannel}
		if midentifier != None:
			if midentifier in mchannel:
				if mchannel != None:
					if mchannel[midentifier] != None: sendto=mchannel[midentifier]
			else:
				if 'all' in mchannel: sendto=mchannel['all']
				else: sendto=[]
		else:
			if 'all' in mchannel:
				sendto=mchannel['all']
			else: sendto=[]
		if 'all' in mchannel:
			for a in mchannel['all']:
				if sendto.count(a) == 0: sendto.append(a)
		for chan in sendto:
			colordi=''
			if cursing and chan.lower() != 'nickserv' and midentifier != 'comment' and midentifier != 'comments':
				if msg.count('My current circuit alcohol level is') == 1: dlevel=dlevel*2
				"""
=======
if len(db['msgqueue']) != 0 and time.time() > lastsent + .3:
    sql.unique_set('data', 'drunklevel', str(int(db['drunklevel']) + 1))
    #[msg,channel (all main db['config']['chans']), type(privmsg),identifier(None)]
    #print db['msgqueue']
    #print db['msgqueue'][0][0]
    db['msgqueue'][0][0] = db['msgqueue'][0][0].encode(
        'ascii', 'ignore').replace('\r', '').replace('\n', '')
    if len(db['msgqueue'][0]) >= 5: cursing = db['msgqueue'][0][4]
    else: cursing = True
    if len(db['msgqueue'][0]) >= 4: midentifier = db['msgqueue'][0][3]
    else: midentifier = None
    if len(db['msgqueue'][0]) >= 3:
        if db['msgqueue'][0][2] == None: mtype = 'PRIVMSG'
        else: mtype = db['msgqueue'][0][2]
    else: mtype = 'PRIVMSG'
    if len(db['msgqueue'][0]) >= 2:
        if db['msgqueue'][0][1] == None: mchannel = db['config']['chans']
        else: mchannel = db['msgqueue'][0][1]
    else: mchannel = db['config']['chans']
    msg = db['msgqueue'][0][0][:550].replace('&nbsp;', ' ')
    abob = ''
    if astrobob: abob = chr(3) + '0,5'
    msg = msg.strip().replace('%ABOB%', abob)
    if abob != '': msg += chr(3)
    #msg, mchannel, mtype, midentifier
    if (lastmsg != msg or time.time() > lastsent + 3 or 1 == 1) and msg != '':
        if isinstance(mchannel, basestring): mchannel = {'all': [mchannel]}
        elif isinstance(mchannel, list): mchannel = {'all': mchannel}
        if midentifier != None:
            if midentifier in mchannel:
                if mchannel != None:
                    if mchannel[midentifier] != None:
                        sendto = mchannel[midentifier]
            else:
                if 'all' in mchannel: sendto = mchannel['all']
                else: sendto = []
        else:
            if 'all' in mchannel:
                sendto = mchannel['all']
            else:
                sendto = []
        if 'all' in mchannel:
            for a in mchannel['all']:
                if sendto.count(a) == 0: sendto.append(a)
        for chan in sendto:
            colordi = ''
            if cursing and chan.lower(
            ) != 'nickserv' and midentifier != 'comment' and midentifier != 'comments':
                if msg.count('My current circuit alcohol level is') == 1:
                    dlevel = dlevel * 2
                """
>>>>>>> origin/master
				#drunksettings ->
					curse
					names
					appendages
					toodrunk
					duplicate
					slur
					insert
					SUBS:
						randomize
						min
			"""
<<<<<<< HEAD
				if random.randrange(0,db['drunksettings']['curse']['randomize']) < dlevel and msg.count(' ') > 2 and dlevel > db['drunksettings']['curse']['min']:
					pt=random.randrange(0,len(msg)-1)
					loopcmsg=0
					while msg[pt] != ' ' and msg[pt] and loopcmsg < 10:
						pt=random.randrange(0,len(msg)-1)
						loopcmsg+=1
					curse=random.choice(db['language']['curses'])
					msg=msg[:pt]+' '+curse.upper()+' '+msg[pt+1:]
				namecalled=False
				if random.randrange(0,db['drunksettings']['names']['randomize']) < dlevel and dlevel > db['drunksettings']['names']['min']:
					addition=random.choice(db['language']['names']).upper()
					if msg[-1] == '.': msg=msg[:-1]
					plu=''
					if midentifier=='score': plu='S'	
					rannum=random.randrange(0,5)	
					if rannum == 2: msg=addition+plu+', here\'s what\'s up. '+msg+'!'*random.randrange(1,15) 
					elif rannum==3 or rannum==4: addition+plu+', '+msg
					else: msg=msg+' you '+addition+plu+'!'*random.randrange(1,15)
					namecalled=True
				if not namecalled and random.randrange(0,db['drunksettings']['appendages']['randomize']) < dlevel and dlevel > db['drunksettings']['appendages']['min']:
					appendage=random.choice(db['language']['appendages']).strip()
					if appendage[-1]=='-': msg=appendage[:-1]+' '+msg
					elif appendage[0]=='-': msg=msg+' '+appendage[1:]
					else: msg=random.choice([msg+' '+appendage+'!'*random.randrange(1,10),appendage+'!'*random.randrange(0,3)+' '+msg])
				if random.randrange(0,db['drunksettings']['toodrunk']['randomize']) < dlevel and dlevel >= db['drunksettings']['toodrunk']['min']:
					msg+=random.choice(db['language']['toodrunk'])
				cedit=0
				while cedit <=10:
					cedit+=1
					if len(msg) > 3 and random.randrange(0,db['drunksettings']['duplicate']['randomize']) < dlevel and dlevel > db['drunksettings']['duplicate']['min']:
						pt=random.randrange(0,len(msg)-1)
						if ctnums(msg[pt]) == 0 and msg[pt] != ',' and (msg[:pt].count('*') == 0 or msg[pt:].count('*') == 0): msg=msg[:pt]+msg[pt]+msg[pt:]
				if random.randrange(0,db['drunksettings']['slur']['randomize']) < dlevel and msg.strip().count(' ') != 0 and dlevel > db['drunksettings']['slur']['min']:
					print 'hmph'
					strep=0
					enrep=0
					loopcspc=0
					while (msg[strep:]+msg[:enrep]).count(' ') == 0 and loopcspc < 500:
						loopcspc+=1
						strep=random.randrange(0,len(msg))
						enrep=strep+random.randrange(0,3)
					if ctnums(msg[strep:enrep]) == 0 and (msg[:strep].count('*') == 0 or msg[enrep:].count('*') == 0): msg=msg[:strep]+msg[enrep:]
				cedit=1
				while cedit <= 4:
					cedit+=3
					if random.randrange(0,db['drunksettings']['insert']['randomize']) < dlevel and dlevel > db['drunksettings']['insert']['min']:
						randadd=''
						randlen=random.randrange(1,3)
						while len(randadd) < randlen:
							randadd+=random.choice(['a','e','i','o','u'])
						strep=random.randrange(0,len(msg))
						enrep=strep+random.randrange(0,3)
						if ctnums(msg[strep:enrep]) == 0 and (msg[:strep].count('*') == 0 or msg[:enrep].count('*') == 0): msg=msg[:strep]+randadd+msg[enrep:]
				
	#		if msg.count(chr(3)) == 0 and chan.lower() != 'nickserv': colordi=chr(3)+'0,1'	
			h=HTMLParser()
			if astrobob: colordi=chr(3)+'0,5'
#			msg='test'
			s.send(mtype+" "+chan+" :"+colordi+h.unescape(msg.replace('*','').encode('ascii','ignore'))+"\r\n")
			#print mtype+" "+chan+" :"+colordi+msg.encode('ascii','ignore')
			open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+': sent to '+chan+": "+colordi+msg+"\r\n")
			#open('logs/interactw.log','a').write(time.strftime('%a %b %d %H:%M')+': sent to '+chan+": "+colordi+msg+"\r\n")
	db['msgqueue'].pop(0)
	lastsent=time.time()
	lastmsg=msg
#loop_time=time.time()-this_loop_start_time
=======
                if random.randrange(0, db['drunksettings']['curse'][
                        'randomize'
                ]) < dlevel and msg.count(
                        ' ') > 2 and dlevel > db['drunksettings']['curse'][
                                'min'
                        ]:
                    pt = random.randrange(0, len(msg) - 1)
                    loopcmsg = 0
                    while msg[pt] != ' ' and msg[pt] and loopcmsg < 10:
                        pt = random.randrange(0, len(msg) - 1)
                        loopcmsg += 1
                    curse = random.choice(db['language']['curses'])
                    msg = msg[:pt] + ' ' + curse.upper() + ' ' + msg[pt + 1:]
                namecalled = False
                if random.randrange(0, db['drunksettings']['names'][
                        'randomize'
                ]) < dlevel and dlevel > db['drunksettings']['names']['min']:
                    addition = random.choice(db['language']['names']).upper()
                    if msg[-1] == '.': msg = msg[:-1]
                    plu = ''
                    if midentifier == 'score': plu = 'S'
                    rannum = random.randrange(0, 5)
                    if rannum == 2:
                        msg = addition + plu + ', here\'s what\'s up. ' + msg + '!' * random.randrange(
                            1, 15)
                    elif rannum == 3 or rannum == 4:
                        addition + plu + ', ' + msg
                    else:
                        msg = msg + ' you ' + addition + plu + '!' * random.randrange(
                            1, 15)
                    namecalled = True
                if not namecalled and random.randrange(
                        0, db['drunksettings']['appendages'][
                                'randomize'
                        ]) < dlevel and dlevel > db['drunksettings']['appendages'][
                                'min'
                        ]:
                    appendage = random.choice(db['language']['appendages'
                                           ]).strip()
                    if appendage[-1] == '-': msg = appendage[:-1] + ' ' + msg
                    elif appendage[0] == '-': msg = msg + ' ' + appendage[1:]
                    else:
                        msg = random.choice(
                            [msg + ' ' + appendage + '!' * random.randrange(
                                1, 10), appendage + '!' * random.randrange(0, 3)
                             + ' ' + msg])
                if random.randrange(0, db['drunksettings']['toodrunk'][
                        'randomize'
                ]) < dlevel and dlevel >= db['drunksettings']['toodrunk']['min']:
                    msg += random.choice(db['language']['toodrunk'])
                cedit = 0
                while cedit <= 10:
                    cedit += 1
                    if len(msg) > 3 and random.randrange(
                            0, db['drunksettings']['duplicate'][
                                    'randomize'
                            ]) < dlevel and dlevel > db['drunksettings']['duplicate'][
                                    'min'
                            ]:
                        pt = random.randrange(0, len(msg) - 1)
                        if ctnums(msg[pt]) == 0 and msg[pt] != ',' and (
                                msg[:pt].count('*PR*') == 0 or
                                msg[pt:].count('*PR*') == 0):
                            msg = msg[:pt] + msg[pt] + msg[pt:]
                if random.randrange(0, db['drunksettings']['slur'][
                        'randomize'
                ]) < dlevel and msg.strip().count(
                        ' ') != 0 and dlevel > db['drunksettings']['slur'][
                                'min'
                        ]:
                    print 'hmph'
                    strep = 0
                    enrep = 0
                    loopcspc = 0
                    while (msg[strep:] + msg[:enrep]
           ).count(' ') == 0 and loopcspc < 500:
                        loopcspc += 1
                        strep = random.randrange(0, len(msg))
                        enrep = strep + random.randrange(0, 3)
                    if ctnums(msg[strep:enrep]) == 0 and (
                            msg[:strep].count('*PR*') == 0 or
                            msg[enrep:].count('*PR*') == 0):
                        msg = msg[:strep] + msg[enrep:]
                cedit = 1
                while cedit <= 4:
                    cedit += 3
                    if random.randrange(0, db['drunksettings']['insert'][
                            'randomize'
                    ]) < dlevel and dlevel > db['drunksettings']['insert'][
                            'min'
                    ]:
                        randadd = ''
                        randlen = random.randrange(1, 3)
                        while len(randadd) < randlen:
                            randadd += random.choice(['a', 'e', 'i', 'o', 'u'])
                        strep = random.randrange(0, len(msg))
                        enrep = strep + random.randrange(0, 3)
                        if ctnums(msg[strep:enrep]) == 0 and (
                                msg[:strep].count('*PR*') == 0 or
                                msg[:enrep].count('*PR*') == 0):
                            msg = msg[:strep] + randadd + msg[enrep:]
>>>>>>> origin/master

                #		if msg.count(chr(3)) == 0 and chan.lower() != 'nickserv': colordi=chr(3)+'0,1'
            h = HTMLParser()
            if astrobob: colordi = chr(3) + '0,5'
            #			msg='test'
            s.send(mtype + " " + chan + " :" + colordi + h.unescape(msg.replace(
                '*PR*', '').encode('ascii', 'ignore')) + "\r\n")
            #print mtype+" "+chan+" :"+colordi+msg.encode('ascii','ignore')
            open('logs/interact.log',
                 'a').write(time.strftime('%a %b %d %H:%M') + ': sent to ' +
                            chan + ": " + colordi + msg + "\r\n")
            #open('logs/interactw.log','a').write(time.strftime('%a %b %d %H:%M')+': sent to '+chan+": "+colordi+msg+"\r\n")
    db['msgqueue'].pop(0)
    lastsent = time.time()
    lastmsg = msg
#if time.time()-this_loop > .2: print time.time()-this_loop

<<<<<<< HEAD
sql.unique_set('data','msgqueue',json.dumps(db['msgqueue']))
=======
sql.unique_set('data', 'msgqueue', json.dumps(db['msgqueue']))
time.sleep(.9)
>>>>>>> origin/master
