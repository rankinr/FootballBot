"""
Returns team record and schedule.
"!info" can be replaced with "?" (i.e., "?UMiami" will produce the same result as "!info UMiami")
"""


mech = Browser()


#what team do you want to know about?

def abbrev(words,abb,debug=False):
	con=abb
	print words
	for throw,ws in con.iteritems():
		#print words.lower()+'.'+ws[0].lower()+'.'
		if ws[0] != None and words.lower().strip()==ws[0].lower().strip(): words=ws[1]
		#if debug: print words+'.'+ws[0]+'.'+ws[1]+'.'
	return words
if (origin.count('|') != 0 or origin.count('[') != 0) and ''.join(params).strip() == '':
	if origin.count('|') != 0: newo=origin[origin.find('|')+1:]
	elif origin.count('[') != 0: newo=origin[origin.find('[')+1:origin.find(']')]
	if newo.strip() != '': params=[newo]
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
	else: db['msgqueue'].append([origin+': Could not find that team.',dest,'PRIVMSG',None])


schedule=[]
if foundMatch:
	
	page = mech.open('http://espn.go.com/college-football/team/schedule/_/id/'+str(teams[closests]))
	html = page.read()
	soup = BeautifulSoup(html)
	table = soup.find("table", attrs={'class':'tablehead'})
	rows=table.findAll('tr',attrs={'class':['evenrow','oddrow']})
	for row in rows:
		cols=row.findAll('td')
		date=cols[0].contents[0].strip()
		opp=cols[1].getText().replace('*','').strip()
		opp=opp.replace('vs','vs. ').replace('@','@ ')
		if opp.count('#') != 0:
			opp2=opp[opp.find('#'):]
			opp2=opp2[opp2.find(' '):].strip()
			opp=opp[:opp.find('#')].strip()+' '+opp2
		schedule.append(date+': '+opp)
	m2s='Schedule for '+closests+': '+', '.join(schedule)
	if len(m2s) > 320:
		m2s=m2s[:320][::-1]
		m2s=m2s[m2s.find(':')+1:]
		m2s=m2s[m2s.find(',')+1:]
		m2s=m2s[m2s.find(',')+1:][::-1]
	db['msgqueue'].append([m2s,dest,'PRIVMSG',None])
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