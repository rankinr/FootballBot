
import re,urllib,os,fcntl,json
a=urllib.urlopen('http://espn.go.com/college-football/teams').read()
a=a[a.find('<div class="mod-header stathead"><h4>FBS (Division I-A Teams)</h4></div>')+len('<div class="mod-header stathead"><h4>FBS (Division I-A Teams)</h4></div>'):a.find('<div class="mod-header stathead"><h4>FCS (Division I-AA Teams)</h4></div>')]
c=0
fdb=open('/home/fbbot/cfb/db.json','r')
fcntl.flock(fdb, fcntl.LOCK_EX)
db=json.load(fdb)
try:
	if not 'teams' in db: db['teams']={}
	while a.count('<div class="mod-header colhead">') != 0 and c < 1000:
		c+=1
		if a.count('<div class="mod-header colhead">') == 1: thisconf=a[a.find('<div class="mod-header colhead">')+len('<div class="mod-header colhead">'):]
		else:
			thisconf=a[a.find('<div class="mod-header colhead">')+len('<div class="mod-header colhead">'):]
			thisconf=thisconf[:thisconf.find('<div class="mod-header colhead">')]
		confname=thisconf[thisconf.find('<h4>')+4:thisconf.find('</h4>')]
		print confname
		while thisconf.count('http://espn.go.com/college-football/team/_/id') != 0:
			thisch=thisconf[thisconf.find('http://espn.go.com/college-football/team/_/id/')+len('http://espn.go.com/college-football/team/_/id/'):]
			thisconf=thisch
			sid=thisch[:thisch.find('/')]
			snm=thisch[thisch.find('">')+2:]
			snm=snm[:snm.find('</a>')]
			print '\t'+snm+': '+sid
			db['teams'][snm]=sid
		a=a[a.find('<div class="mod-header colhead">')+len('<div class="mod-header colhead">'):]
except:
	fcntl.flock(fdb, fcntl.LOCK_UN)
	print 'ERROR'
open('/home/fbbot/cfb/db.json','w').write(json.dumps(db))
fcntl.flock(fdb, fcntl.LOCK_UN)
