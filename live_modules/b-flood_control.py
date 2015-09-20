for a,b in pastcmd.iteritems():
	for c in b:
		if c < time.time()-60: b.pop(b.index(c)) # removes tracking after 60 seconds
for a,b in user_messages.iteritems():
	for c in b:
		if c < time.time()-10: b.pop(b.index(c))
	if len(b) > 5 and time.time() > last_alert+60:
		last_alert=time.time()
		db['msgqueue'].append(['Flood alert: '+a,''])