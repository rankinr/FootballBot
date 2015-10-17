from mechanize import Browser
from bs4 import BeautifulSoup

mech = Browser()

url = "http://espn.go.com/college-football/lines"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html,"html5lib")
tables = soup.findAll("table", {'class':'tablehead'})
import re,urllib,os,fcntl,json

db={}

exec(open('/home/fbbot/cfb/sload.py').read())

sql.cur.execute("""select * from data""")
a=sql.cur.fetchall()
for b in a:
	if a[1] != '' and a[1] != None:
		if a.count('language') == 0: db[b[0]]=json.loads(b[1])
		else: db['language'][b[0][b[0].find('language-')+len('language-'):]]=json.loads(b[1])
db['spread']={}

rows=tables[0].findAll('tr')
for row in rows:
	team=''
	try:
		if row['class'].count('stathead') != 0:
			teams=row.find('td').contents
			teams=teams[0]
			neutral=True
			print teams
			if teams.count(' at ') == 1:
				neutral=False
				jnr=' at '
			elif teams.count(' vs ') == 1: jnr=' vs '
			team1=teams[:teams.find(jnr)].strip()
			team2=teams[teams.find(jnr)+4:teams.find(' - ')].strip()
			if team1[0]=='#': team1=team1[team1.find(' ')+1:].strip()
			if team2[0]=='#': team2=team2[team2.find(' ')+1:].strip()
			if team1+team2 in db['games_new']['fbs']: gident=team1+team2
			elif team2+team1 in db['games_new']['fbs']: gident=team2+team1
		else:
			cols=row.findAll('td')
			#if gident.count('North Carolina') != 0: print gident+cols[0].contents[0].strip()
			ou='NA'
			for col in cols:
				colt=col.getText()
				if colt.count('O/U') != 0:
					#print colt
					ou=colt[::-1]
					ou=ou[ou.find('O/U'[::-1]):].strip()[::-1]
					#print ou
			if cols[0].contents[0]=='BETONLINE.ag':
				c2=cols[2].renderContents()
				c3=cols[3].renderContents()
#				print c2
#				print c3
				first=c3[:c3.find('<')].strip()+' '
				second=c3[c3.find('>')+1:].strip()+' '
				first+=c2[:c2.find('<')].strip()
				second+=c2[c2.find('>')+1:].strip()
#				print first
#				print second
				db['spread'][gident]=first+', '+second+', '+ou
				db['games_new']['fbs'][gident]['neutral']=neutral
	except:
		aewe=1
sql.unique_set('data','spread',json.dumps(db['spread']))
sql.unique_set('data','games',json.dumps(db['games_new']['fbs']))
