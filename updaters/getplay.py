import urllib, json

pg=urllib.urlopen('http://espn.go.com/college-football/scoreboard').read()
pg=json.loads(pg[pg.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):pg.find(';window.espn.scoreboardSettings')])

#print json.dumps(pg['events'][0])
for a in pg['events']:
	if 'situation' in a['competitions'][0]:
		down=a['competitions'][0]['situation']['downDistanceText']
		gid=a['id']
		now=a['status']['type']['shortDetail']
		most_recent_play=a['competitions'][0]['situation']['lastPlay']['text']
		print 'ID: '+gid
		print 'Down: '+down
		print 'Now: '+now
		print 'Most recent play: '+most_recent_play