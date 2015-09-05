import urllib, bs4
from bs4 import BeautifulSoup
import  json
db={}
mysql_host='localhost'
mysql_user='fbbot'
mysql_password='QP9pqh5UR7MsPSx5NL6fgmCVz4fr4hdN28Kp9xD5r3GsemntJZ'
mysql_db='fbbot_old'
exec(open('/home/fbbot/cfb/sload.py').read())
sql.cur.execute("""select * from data""")
a=sql.cur.fetchall()
db['language']={}
for b in a:
	if b[0]=='drunklevel' or b[0] =='drunksetting':
		if b[0] == 'drunklevel': db[b[0]]=int(b[1])
		else: db[b[0]]=b[1]
	elif b[0]=='msgqueue':
		db['msgqueue']=json.loads(b[1])
	else:
		if b[0].count('language') == 0: db[b[0]]=json.loads(b[1])
		else:
			db['language'][b[0][b[0].find('language-')+len('language-'):]]=json.loads(b[1])

def k4v(v,ar):
	toret=''
	for a,b in ar.iteritems():
		if b == v:
			toret=a
	return toret
def stats(gid):
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
print stats('400603835')