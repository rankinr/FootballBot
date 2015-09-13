for a,b in pastcmd.iteritems():
	for c in b:
		if c < time.time()-60: b.pop(b.index(c)) # removes tracking after 60 seconds