import MySQLdb
mysql_host=''
mysql_user=''
mysql_password=''
mysql_db=''

l_mysql_refresh=0

class mysql:
	def __init__(self):
		self.db=MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_password,db=mysql_db)
		self.db.autocommit(True) # Rather than reconnecting on each loop
		self.cur=self.db.cursor()
	def unique_set(self, table, type, new_value):
		self.cur.execute("""select %s_type from %s where %s_type="%s" limit 1;""" % (table, table, table, type))
		if self.cur.rowcount == 0:
			self.cur.execute("""INSERT INTO  %s (`%s_type` ,`%s_value`)VALUES ("%s",  "%s");""" % (table, table, table, type, MySQLdb.escape_string(new_value)))
		else: 
			self.cur.execute("""update %s set %s_value="%s" where %s_type="%s" limit 1;"""				% (table, table, MySQLdb.escape_string(new_value), table, type))
	def unique_get(self,table,type):
		self.cur.execute("""select %s_value from %s where %s_type="%s" limit 1;""" % (table,table,table,type))
		a=self.cur.fetchall()
		if len(a) == 0: return False
		else: return a[0][0]
sql=mysql()