# LOADS MYSQL INFORMATION

if not sql.db.open or l_mysql_refresh < time.time()-3600:
	sql=mysql()
	l_mysql_refresh=time.time()

db['language'] = {}
if not 'msgqueue' in db: db['msgqueue']=[]

sql.cur.execute("""select * from data""")
a=sql.cur.fetchall()
for b in a:
	if b[0]=='drunklevel' or b[0] =='drunksetting':
		if b[0] == 'drunklevel': db[b[0]]=int(b[1])
		else: db[b[0]]=b[1]
	else:
		if b[0].count('language') == 0: db[b[0]]=json.loads(b[1])
		else:
			db['language'][b[0][b[0].find('language-')+len('language-'):]]=json.loads(b[1])