import urllib2,re,string,urllib,time,unicodedata,json,os,fcntl
urllib.urlcleanup()
st=time.time()
keepgoing=True
while keepgoing and time.time() < st+60*9.5:
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'robs reddit irc robot')]
	ourlisting=json.loads(opener.open('http://www.reddit.com/r/CFB/search.json?q=title%3AGame+Thread&restrict_sr=on&t=day&sort=top').read())
	#ourlisting=json.load(open('savebw'))
	gtr = re.compile(re.escape('game thread'), re.IGNORECASE)
	ourlisting['data']['children']=ourlisting['data']['children'][:10]
	cmtsar=[]
	for id in ourlisting['data']['children']:
		score=id['data']['score']
		title=id['data']['title'].replace('&amp;','&')	
		#print title
		title=re.sub(r'\([^)]*\)', '',gtr.sub('',title.replace('[','').replace(']',''))).strip()
		url=id['data']['url']	
		if score > 3:
			cmts=json.loads(opener.open(url+'.json?sort=new&throw='+str(time.time())).read())[1]['data']['children']
			for cmt in cmts:
				isMain=True
				try: wur=cmt['data']['body']
				except: isMain=False
				if isMain:
					thiscmt=cmt['data']['body']
					thiscmt=unicodedata.normalize('NFKD', thiscmt).encode('ascii','ignore')
					thiscmt=str(thiscmt[:150]).replace('\r',' ').replace('\n',' ').replace('\t',' ').replace('\x0b',' ').replace('\x0c',' ').replace(':','')
					while thiscmt.count('  ') != 0: thiscmt=thiscmt.replace('  ',' ')
					if len(cmt['data']['body']) > 150:
						thiscmt=thiscmt[::-1][thiscmt[::-1].find(" "):][::-1]+'...'
					thiscmt=thiscmt.strip()
					cscore=cmt['data']['ups']-cmt['data']['downs']
					created=cmt['data']['created_utc']
					if cscore >= 2.5: scoreval=cscore/((time.time()-created)/60)
					else: scoreval=0
					oldcmts=open('/home/fbbot/cfb/updaters/.oldcmts').read()
					if scoreval >= 4.2 and oldcmts.count(':'+cmt['data']['id']+':') == 0:
						#[msg,channel (all main chans), type(privmsg),identifier(None)]
						#print thiscmt
						thiscmt=thiscmt.replace('&amt;','&')
						cmtsar.append(['"'+thiscmt+'" -'+cmt['data']['author']+' ('+title+')',None,None,'comments'])
						open('/home/fbbot/cfb/updaters/.oldcmts','a').write(':'+cmt['data']['id']+':')
	fdb=open('/home/fbbot/cfb/db.json','r')
	fcntl.flock(fdb, fcntl.LOCK_EX)
	db=json.load(fdb)
	if json.dumps(db['games']).count('team1score') == json.dumps(db['games']).count('PM ET')+json.dumps(db['games']).count('AM ET') or json.dumps(db['games']).count('team1score') == json.dumps(db['games']).count('DELAYED')+json.dumps(db['games']).count('PM ET')+json.dumps(db['games']).count('FINAL'):
		keepgoing=False
	try:
		for a in cmtsar:
			db['msgqueue'].append(a)
			for u in db['cmts_following']:
				db['msgqueue'].append([a[0],u,'NOTICE','comment'])
		#db['msgqueue'].append(['test',None,None,'comments'])
	except:
		fcntl.flock(fdb, fcntl.LOCK_UN)
	open('/home/fbbot/cfb/db.json','w').write(json.dumps(db))
	fcntl.flock(fdb, fcntl.LOCK_UN)
	time.sleep(40)
#print title+str(score)
"""if len(cmtsscores) != 0:
	if len(cmtsscores) < 10: minval=sorted(cmtsscores)[::-1][-1]
	else: minval=sorted(cmtsscores)[::-1][9]
	oldcmts=open('/home/rob/cfb/.oldcmts').read()
	for cmt in cmtsar:
		if cmt[1] >= minval and oldcmts.count(':'+cmt[2]+':') == 0:
			open('/home/rob/cfb/.oldcmts','a').write(':'+cmt[2]+':')
			mqa('"'+cmt[0]+'" -'+cmt[4]+' ('+cmt[3]+')')"""
