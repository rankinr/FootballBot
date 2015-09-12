"""Under construction. The goal is to make a webpage where you can go to set things like teams you are following for the bot to update you on, etc."""

code=''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(10))
sql.cur.execute("""select %s from %s where %s="%s" limit 1;""" % ('mid', 'me', 'username', origin))
if sql.cur.rowcount == 0:
	sql.cur.execute("""INSERT INTO  %s (`%s` ,`%s`)VALUES ("%s",  "%s");""" % ('me', 'username', 'access_code',MySQLdb.escape_string(origin),MySQLdb.escape_string(code)))
else: 
	sql.cur.execute("""update %s set %s="%s" where %s="%s" limit 1;"""				% ('me', 'access_code', MySQLdb.escape_string(code), 'username', MySQLdb.escape_string(origin)   ))
db['msgqueue'].append(['Your link is: http://fbbot.robrankin.com/me.php?c='+code,origin])