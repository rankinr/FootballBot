"""
Returns team record and schedule.
"!info" can be replaced with "?" (i.e., "?UMiami" will produce the same result as "!info UMiami")
"""


mech = Browser()

if dest.lower()=='footballbot': msg_dest=origin
else: msg_dest=dest

user_pref=sql.get_user(origin)
msg_type='PRIVMSG'
if user_pref:
	if 'cmds' in user_pref and 'info' in user_pref['cmds']:
		if user_pref['cmds']['info']=='you': msg_dest=origin
		elif user_pref['cmds']['info']=='channel' and dest.lower()!='footballbot': msg_dest=dest
	if 'pers_msgs' in user_pref and msg_dest==origin:
		if user_pref['pers_msgs'] == 'notice': msg_type='NOTICE'
		elif user_pref['pers_msgs'] == 'message': msg_type='PRIVMSG'

#what team do you want to know about?

def gameWeek(date):
	week=False
	if date.count(',') != 0: date=date[date.find(',')+1:].strip()
	yr=str(time.localtime()[0])
	if time.localtime()[1] != 1 and date.count('Jan') != 0: yr=str(time.localtime()[0]+1) # may need to adjust if playoff timetable is ever changed substantially
	this_date_time=time.mktime(time.strptime(date+' '+yr,'%b %d %Y'))+3600*10
	startTime=1441252801  	#will have to change for next season - this is Sept 3, 2015
	c=0
	lval=0
	while c < 20 and not week:
		c+=1
		if this_date_time < startTime+3600*24*7*c: week=c
		else: lval=c
	if week > db['all_ranks']['last_week']: week=db['all_ranks']['last_week']
	print str(week)
	return str(week)
def abbrev(words,abb,debug=False):
	con=abb
	for throw,ws in con.iteritems():
		#print words.lower()+'.'+ws[0].lower()+'.'
		if ws[0] != None and words.lower().strip()==ws[0].lower().strip(): words=ws[1]
		#if debug: print words+'.'+ws[0]+'.'+ws[1]+'.'
	return words
if (origin.count('|') != 0 or origin.count('[') != 0) and ''.join(params).strip() == '':
	if origin.count('|') != 0: newo=origin[origin.find('|')+1:]
	elif origin.count('[') != 0: newo=origin[origin.find('[')+1:origin.find(']')]
	if newo.strip() != '': params=[newo]
confs_list={'AAC':'American Athletic Conference','ACC':'Atlantic Coast Conference','BIG 12':'Big 12 Conference','BIG12':'Big 12 Conference','BIG TEN':'Big Ten Conference','BIG 10':'Big Ten Conference','BIG TEN':'Big10 Conference','B1G':'Big Ten Conference','CUSA':'Conference USA','MID-AMERICAN':'Mid-American Conference','MIDAMERICAN':'Mid-American Conference','MID AMERICAN':'Mid-American Conference','MW':'Mountain West Conference','MWC':'Mountain West Conference','MOUNTAINWEST':'Mountain West Conference','PAC12':'Pac-12 Conference','PAC-12':'Pac-12 Conference','SEC':'Southeastern Conference','SUNBELT':'Sun Belt Conference','SUN BELT':'Sun Belt Conference'}
if ''.join(params).strip().upper() in confs_list:
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
	ourconf=confs[confs_list[''.join(params).upper()]]
	to_send=''
	def gtRks(tl): #tl=teamlist
		c=0
		rks_int=[int(x) for x in tl]
		rks_int.sort()
		cur_ts='' #cur to_send (to be appended to to_send)
		for rk in rks_int:
			team=tl[str(rk)]
			c+=1
			cur_ts+=str(c)+'. '+team+' | '
		return cur_ts[:-3]
			
	to_send+='\x02'+confs_list[''.join(params).upper()]+' Standings\x02:'
	if len(ourconf) < 4: #subconf
		for subconf in ourconf:
			c=0
			to_send+=' \x02'+subconf+':\x02 '
			to_send+=gtRks(ourconf[subconf])
	else: to_send+=' '+gtRks(ourconf)
	for a in splitMessage(to_send,split=' | ',l=450):
			db['msgqueue'].append([a,msg_dest,msg_type,None])
else:
	if ''.join(params).strip() != '':
		tbyname={}
		closestval=1000000
		closests=''
		teams=db['teams']
		params=abbrev(' '.join(params).lower(),db['abbreviations'])
		for a,b in teams.iteritems():
			if a != 'lastupdate':
				if params.count(' ') == 0: tclv=closest([params.lower(),params.lower()+' StateZ'],[a.lower()])
				else: tclv=closest([params.lower(),params.lower().replace('st','state')],[a.lower()])
				if tclv < closestval:
					closestval=tclv
					closests=a
		if dest=='footballbot' or dest=='footballtestbot': dest=origin
		foundMatch=False
		if closests != '' and closestval <= 3:
			foundMatch=True
		else: db['msgqueue'].append([origin+': Could not find that team.',msg_dest,msg_type,None])


	schedule=[]
	if foundMatch:
		
		page = mech.open('http://espn.go.com/college-football/team/schedule/_/id/'+str(teams[closests]))
		html = page.read()
		soup = BeautifulSoup(html)
		wins=str(soup).count('game-status win')
		losses=str(soup).count('game-status loss')
		#record=soup.find('div',{'class':'sub-title'}).getText()
		record=str(wins)+'-'+str(losses)
		table = soup.find("table", attrs={'class':'tablehead'})
		rows=table.findAll('tr',attrs={'class':['evenrow','oddrow']})
		for row in rows:
			row_t=str(row)
			wl=''
			if row_t.count('game-status win') == 1: wl=chr(3)+'3\x02W\x02'+chr(3)+' '
			elif row_t.count('game-status loss') == 1: wl=chr(3)+'4\x02L\x02'+chr(3)+' '
			cols=row.findAll('td')
			if len(cols) > 1: 
				date=cols[0].contents[0].strip().replace('Sept','Sep')
				opp=cols[1].getText().replace('*','').strip()
				opp=opp.replace('vs','vs. ').replace('@','@ ')
				if opp.count('#') != 0:
					opp2=opp[opp.find('#'):]
					opp2=opp2[opp2.find(' '):].strip()
					opp=opp[:opp.find('#')].strip()+' '+opp2
				opp_clean=opp.replace('vs.','').replace('@','').replace('  ',' ').strip()
				if wl != '' and date.count(',') != 0: date=date[date.find(',')+1:].strip()
				rk=''
				wk=gameWeek(date)
				print opp_clean
				if opp_clean in db['all_ranks']: print opp_clean+str(db['all_ranks'][opp_clean])
				if opp_clean in db['all_ranks'] and wk in db['all_ranks'][opp_clean]:
					if opp.count('vs. ') == 1: opp=opp.replace('vs. ','vs. ('+str(db['all_ranks'][opp_clean][gameWeek(date)])+') ')
					elif opp.count('@ ') == 1: opp=opp.replace('@ ','@ ('+str(db['all_ranks'][opp_clean][gameWeek(date)])+') ')
				schedule.append(date+': '+wl+opp)
		m2s=closests+': \x02Record:\x02 '+record+' \x02Schedule:\x02 '+' | '.join(schedule)
		for a in splitMessage(m2s,split=' | ',l=450):
			db['msgqueue'].append([a,msg_dest,msg_type,None])
"""	def gstat(d,stype):
		d=d[d.find('<h4>'+stype+'</h4></div><div class="mod-content"><span class="stat">')+len('<h4>'+stype+'</h4></div><div class="mod-content"><span class="stat">'):]
		stat=d[:d.find('</span')]
		rk=d[d.find('<strong>')+len('<strong>'):d.find('</strong>')]
		return [stat,rk]
	def odata(eweb):
		passing=gstat(eweb,'PASSING YARDS')
		rushing=gstat(eweb,'RUSHING YARDS')
		pfor=gstat(eweb,'POINTS FOR')
		pag=gstat(eweb,'POINTS AGAINST')
		return '\x02Stats:\x02 \x02Passing\x02 '+passing[0]+' ('+passing[1]+') \x02Rushing\x02 '+rushing[0]+' ('+rushing[1]+') \x02Points for\x02 '+pfor[0]+' ('+pfor[1]+') \x02Points against\x02 '+pag[0]+' ('+pag[1]+')'

"""