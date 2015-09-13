if time.localtime()[3] == 5:
	sql.unique_set('data','drunklevel',str(0))
	cursedHoya=False
	pastcmd={}
dlevel=0
if db['drunksettings']['active']: dlevel=db['drunklevel']