import urllib, json
a = urllib.urlopen(
    'http://scores.espn.go.com/college-football/scoreboard/_/group/81/year/2015/seasontype/2/').read(
    )
a = a[a.find('window.espn.scoreboardData'):]
print a
a = json.loads(a[a.find('{'):a.find('</script>')].strip())

for b in a:
    print b
"""



def isoTyp(txt,typ):
	txt=txt[txt.find('-'+typ+'"'):]
	txt=txt[txt.find('">')+2:]
	while txt[0]=='<': txt=txt[txt.find('>')+1:]
	return txt[:txt.find('<')].replace('&nbsp',' ').strip()

data={}
dtypes={'status':'statusText','ntwk':'preTV','team1':'aTeamName','team1score':'aTotal','team2':'hTeamName','team2score':'hTotal'}

while a.count('<div class="game-header">') != 0:
	a=a[a.find('<div class="game-header">')+len('<div class="game-header">'):]
	cura=a[:a.find('-leadersHeader">Game Leaders</h5>')]
	curd={}
	for b,c in dtypes.iteritems():
		curd[b]=isoTyp(cura,c)
	gid=cura[:cura.find('-statusText"')]
	gid=gid[::-1][:gid[::-1].find('"')][::-1]
	curd['gid']=gid
	data[curd['team1']+curd['team2']]=curd
	
	
	
exec(open('/home/fbbot/cfb/sload.py').read())

sql.unique_set('data','fcs',json.dumps(data))	

"""
