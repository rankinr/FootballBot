import MySQLdb
mysql_host=''
mysql_user=''
mysql_password=''
mysql_db=''

l_mysql_refresh=0

try: 
	pre_g=prefix # multiple rows for multiple servers, to have multiple instances running at same time
except:
	pre_g=''
class mysql:
	def __init__(self):
		self.db=MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_password,db=mysql_db)
		self.db.autocommit(True) # Rather than reconnecting on each loop
		self.cur=self.db.cursor()
	def unique_set(self, table, type, new_value,pre=''):
		if pre=='' and pre_g != '': pre=pre_g
		self.cur.execute("""select %s_type from %s where %s_type="%s" limit 1;""" % (table, pre+table, table, type))
		if self.cur.rowcount == 0:
			self.cur.execute("""INSERT INTO  %s (`%s_type` ,`%s_value`)VALUES ("%s",  "%s");""" % (pre+table, table, table, type, MySQLdb.escape_string(new_value)))
		else: 
			self.cur.execute("""update %s set %s_value="%s" where %s_type="%s" limit 1;"""				% (pre+table, table, MySQLdb.escape_string(new_value), table, type))
	def unique_get(self,table,type,pre=''):
		if pre=='' and pre_g != '': pre=pre_g
		self.cur.execute("""select %s_value from %s where %s_type="%s" limit 1;""" % (table,pre+table,table,type))
		a=self.cur.fetchall()
		if len(a) == 0: return False
		else: return a[0][0]
	def get_user(self,username,pre=''):
		if pre=='' and pre_g != '': pre=pre_g
		if pre != '': return False
		else:
			self.cur.execute("""select message_settings from me where username='%s' limit 1;""" % (MySQLdb.escape_string(username)))
			a=self.cur.fetchall()
			if len(a) == 0: return False
			else: return json.loads(a[0][0])
sql=mysql()