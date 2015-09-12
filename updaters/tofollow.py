import re,urllib,os,fcntl,json,urllib2,string,time,unicodedata
urllib.urlcleanup()
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'robs reddit irc robot')]
ourlisting=json.loads(opener.open('http://www.reddit.com/r/CFB/search.json?q=title%3AGame+Thread&restrict_sr=on&t=day&sort=top').read())
#ourlisting=json.load(open('savebw'))
gtr = re.compile(re.escape('game thread'), re.IGNORECASE)
others=ourlisting['data']['children'][7:]
ourlisting['data']['children']=ourlisting['data']['children'][:4]
cmts2send=[]
for id in ourlisting['data']['children']:
	score=id['data']['score']
	tid=id['data']['id']
	title=id['data']['title']	
	title=re.sub(r'\([^)]*\)', '',gtr.sub('',title.replace('[','').replace(']',''))).strip()
	url=id['data']['url']	
	if score > 5:
		cmts=json.loads(opener.open(url+'.json?sort=new&throw='+str(time.time())).read())[1]['data']['children']
		for cmt in cmts:
			if 'body' in cmt['data']:
				thiscmt=cmt['data']['body']
				thiscmt=unicodedata.normalize('NFKD', thiscmt).encode('ascii','ignore')
				thiscmt=str(thiscmt[:150]).replace('\r',' ').replace('\n',' ').replace('\t',' ').replace('\x0b',' ').replace('\x0c',' ').replace(':','')
				while thiscmt.count('  ') != 0: thiscmt=thiscmt.replace('  ',' ')
				if len(cmt['data']['body']) > 150:
					thiscmt=thiscmt[::-1][thiscmt[::-1].find(" "):][::-1]+'...'
				thiscmt=thiscmt.strip()
				cscore=cmt['data']['ups']-cmt['data']['downs']
				created=cmt['data']['created_utc']
				if cscore > 4: scoreval=cscore/((time.time()-created)/60)
				else: scoreval=0
				if scoreval > 4:
					#[msg,channel (all main chans), type(privmsg),identifier(None)]
					#print thiscmt
					cmts2send.append([cmt['data']['id'],['"'+thiscmt+'" -'+cmt['data']['author']+' ('+title+')',None,'PRIVMSG','comment']])

try:
	fdb=open('/home/fbbot/cfb/db.json','r')
	fcntl.flock(fdb, fcntl.LOCK_EX)
	db=json.load(fdb)
	for cmt in cmts2send:
		if db['cmtsold'].count(cmt[0]) == 0: 
			db['cmtsold'].append(cmt[0])
			for pers in db['gt_following']:
				newmsg=cmt[1]
				newmsg[1]=pers
				db['msgqueue'].append(newmsg)
	open('/home/fbbot/cfb/db.json','w').write(json.dumps(db))
except:
	fcntl.flock(fdb, fcntl.LOCK_UN)
fcntl.flock(fdb, fcntl.LOCK_UN)