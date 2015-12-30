#PYTHON 3
import urllib,json, time
from bs4 import BeautifulSoup
exec(open('/home/fbbot/cfb/sload.py').read())



confs_site=BeautifulSoup(urllib.urlopen('http://espn.go.com/college-football/standings?t='+str(time.time())),"html5lib")
conferences=confs_site.findAll('div',{'class':'responsive-table-wrap'})
confs={}
for conf in conferences:
	conf_name=conf.find('span',{'class':'long-caption'}).getText()
	confs[conf_name]={}
	subconf=False
	rows=conf.findAll(['thead','tr'])
	c=0
	for row in rows:
		if str(row).count('class="standings-categories"') == 1:
			headings=row.findAll('span')
			for heading in headings:
				heading=heading.getText()
				if heading not in ['Conference','Overall','Polls','CONF','PF','PA','OVER','HOME','ROAD','STRK','AP','USA']:
					subconf=heading
					confs[conf_name][subconf]={}
					c=0
		team=row.find('span',{'class':'team-names'})
		if team != None:
			c+=1
			if subconf: confs[conf_name][subconf][str(c)]=unicode(team.getText()).encode('ascii',errors='ignore').replace('\r','').replace('\n','').replace('San Jos State','San Jose State')
			else: confs[conf_name][str(c)]=unicode(team.getText()).encode('ascii',errors='ignore').replace('\r','').replace('\n','').replace('San Jos State','San Jose State')
sql.unique_set('data','conf_standings',json.dumps(confs))