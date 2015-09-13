c=0
for a in db['msgqueue']:
	if a[0]==None: db['msgqueue'][c]=['Remove','#cfbtest']
	c+=1