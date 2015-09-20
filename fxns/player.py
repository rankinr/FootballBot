"""Returns statistics on player!
Usage: !player <player name> - !player can also be replaced with * (*<player name>)
Examples: *kaaya - *b. kaaya - *brad kaaya"""
if dest.lower() != 'footballbot': origin=dest
players=json.loads(open('/home/fbbot/cfb/players.list').read())

last_names=[]

tstring=' '.join(params).replace('.','')

closest_val=9999
closest_match_name=''
closest_match_url=''
for player in players:
	if tstring.count(' ')==0: p_name=player[0][::-1][:player[0][::-1].find(' ')][::-1].strip()
	else: p_name=player[0]
	pname1=player[0][0]+' '+player[0][player[0].find(' ')+1:]
	diff=min([lev(p_name.lower(),tstring.lower()),lev(pname1.lower(),tstring.lower())])
	if diff < closest_val:
		closest_match_name=player[0]
		closest_match_url=player[1]
		closest_val=diff
if closest_match_url != '' and closest_val <= 10:
	player=BeautifulSoup(urllib.urlopen(closest_match_url),"html5lib")
	player=player.find('table',{'class':'tablehead'})
	headings=player.findAll('tr',{'class':'colhead'})
	heading_list=[]
	doError=False
	if len(headings) == 1: 
		for heading in headings[0].findAll('td'):
			if heading.getText()!='SPLITS': heading_list.append(heading.getText())
	elif len(headings) == 2:
		for heading in headings[1].findAll('td'):
			if heading.getText()!='SPLITS': heading_list.append(heading.getText())
		h2=headings[0].findAll('td')
		h21=h2[1].getText()
		h22=h2[2].getText()
		c=0
		while c < 10:
			if c < 5: heading_list[c]=h21+' '+heading_list[c]
			elif c >= 5: heading_list[c]=h22+' '+heading_list[c]
			c+=1
	else: doError=True
	if not doError:
		rows=player.findAll('tr',{'class':['evenrow','oddrow']})
		c=0
		texts=[]
		for row in rows:
			thisrow=[]
			thisrowtext=''
			lc=-1
			if c < 2:
				cols=row.findAll('td')
				c+=1
				for col in cols:
					if lc==-1: thisrowtext='\x02'+col.getText()+'\x02: '
					else: thisrow.append((heading_list[lc].strip()+': *'+col.getText().strip()+'*').strip())
					lc+=1
				texts.append(thisrowtext+', '.join(thisrow))
		db['msgqueue'].append([closest_match_name+': '+'; '.join(texts),origin])
	else: db['msgqueue'].append(['Sorry, something went wrong. Please let harkatmuld know.',origin])