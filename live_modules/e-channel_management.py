if chansold != db['config']['chans']:
	chansold=db['config']['chans']
	chanlist=[]
	for ctype,chans in db['config']['chans'].iteritems():
		for c in chans:
			if chanlist.count(chans) == 0: chanlist.append(c)
	for chan in chanlist:
		s.send('join %s\r\n' % chan)
		time.sleep(1)
		open('logs/interact.log','a').write(time.strftime('%a %b %d %H:%M')+": I joined "+chan+"\r\n")
		open('logs/interactw.log','a').write(time.strftime('%a %b %d %H:%M')+": I joined "+chan+"\r\n")