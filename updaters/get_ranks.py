"""Pulls rankings from /r/cfb poll once a day."""

import re,urllib,os,fcntl,json
import MySQLdb

exec(open('/home/fbbot/cfb/sload.py').read())


def lev(a,b):
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]
def abbrev(words,abb):
	con=abb
	for ws in con:
		if words.lower().strip()==ws[0].lower().strip(): words=ws[1]
	#if words=='miami': print words+' '+ws[0]
	return words
pg=urllib.urlopen('http://rcfbpoll.com/current-rankings.php').read()
pg=pg[pg.find('<th>PTS</th>'):]
pg=pg[pg.find('<tbody>')+len('<tbody>'):].strip()
pg=pg[:pg.find('</div>')]
main=pg[:pg.find('<strong>')]
mainar=[]
while main.count('</a>') > 0:
	main=main[main.find('</a>')+len('</a>'):]
	main=main[main.find("'>"):]
	curteam=main[2:main.find('</a>')]
	mainar.append(curteam)
	main=main[main.find('</tr>')+4:]
other=pg[pg.find('</strong')+len('</strong>'):]
other=other.split(',')
c=0
for a in other:
	new=a.strip()
	new=new[:-new[::-1].find(' ')-1].strip()
	other[c]=new
	c+=1
rks=mainar+other
#for a in rks:
#	print a

db={}
db['ranks']={}
for a in ['colors','abbreviations']:
	dp=sql.unique_get('data',a)
	db[a]=json.loads(dp)
for a, b in db['colors'].iteritems():
	if not a in db['ranks']: db['ranks'][a]=None
ct=1
for tm in rks:
	tm=abbrev(tm,db['abbreviations']).lower().replace('miami','miami (fl)').replace('ecu','east carolina')
	addd=False
	for a,b in db['ranks'].iteritems():
		if a.lower() == tm.lower():
			db['ranks'][a]=str(ct)
			#print str(ct)+'-'+a+'-'+tm
			addd=True
	if addd==False: print tm+'.'
	ct+=1
sql.unique_set('data','ranks',json.dumps(db['ranks']))
