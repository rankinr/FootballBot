import urllib,json,time,re,fcntl
today=time.strftime('%Y-%m-%d')
z=open('/home/fbbot/cfb/updaters/cp_lastdate').read()
if z != today:
	coachespoll=re.findall('Published On(.*?)</span>',urllib.urlopen('http://www.usatoday.com/sports/ncaaf/polls/').read(),re.DOTALL)[0][1:].strip()
	print coachespoll[:-1]
	print today
	if coachespoll == today:
		try:
			open('/home/fbbot/cfb/updaters/cp_lastdate','w').write(today)
			fdb=open('/home/fbbot/cfb/db.json','r')
			fcntl.flock(fdb, fcntl.LOCK_EX)
			db=json.load(fdb)
			db['msgqueue'].append(['A new Coaches Poll has been released: http://usat.ly/R4IV1R',None,None,'news'])
			open('/home/fbbot/cfb/db.json','w').write(json.dumps(db))
			fcntl.flock(fdb, fcntl.LOCK_UN)
		except: fcntl.flock(fdb, fcntl.LOCK_UN)
