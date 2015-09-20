"""Displays information about me and my commands.
(Are you sure you need to ask about this one? Looks like you've got it already!)"""
if not 'fxnsdir' in cached:
	os.system('ls -lah /home/fbbot/cfb/fxns/ > .fxnsdir')
	cached['fxnsdir']=open('.fxnsdir').read()
	os.system('rm .fxnsdir')
print cached['fxnsdir']
if len(params) != 0:
	#print params[0]+'.py'
	if cached['fxnsdir'].count(params[0].lower()+'.py\n') != 0:
		hf=open('/home/fbbot/cfb/fxns/'+params[0].lower()+'.py').read()
		if hf[0:3]=='"""':
			hf=hf[hf.find('""')+3:]
			hf=hf[:hf.find('""')].split('\n')
			db['msgqueue'].append(['Command !'+params[0],origin,None,None,False])
			for h in hf:
				db['msgqueue'].append(['*'+h+'*',origin])		
		else: db['msgqueue'].append(['I don\'t have any information on that command',origin])
	else: db['msgqueue'].append(['I don\'t have any information on that command',origin])
else:
	for h in db['config']['help']:
		db['msgqueue'].append(['*'+h+'*',origin,None,None,False])