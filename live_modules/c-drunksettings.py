if time.localtime()[3] == 5:
	sql.unique_set('data','drunklevel',str(0))
	db['drunklevel']=0
	cursedHoya=False
	pastcmd={}
dlevel=0
sql.unique_set('data','drunklevel',str(0))
db['drunklevel']=0
if db['drunksettings']['active']:
	if time.localtime()[3] < 21 and time.localtime()[3] > 3: dlevel=pow(db['drunklevel'],1.001)
	else: dlevel=db['drunklevel']+pow(db['drunklevel'],1.2)