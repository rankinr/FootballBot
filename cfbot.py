import json,time,socket,string,random,time,os,hashlib,urllib,sys,traceback,HTMLParser,praw,urllib2
from HTMLParser import HTMLParser
import urlparse,re
from bs4 import BeautifulSoup
from mechanize import Browser
import oauth2 as oauth
import json, operator, math
import httplib
from xml.etree import ElementTree as etree

exec(open('/home/fbbot/cfb/sload.py').read()) # load mysql information
exec(open('/home/fbbot/cfb/common_functions.py')) #load custom functions

announced=[] #to track games whose start has been announced
tmtype='PRIVMSG' # default message type is PRIVMSG
pastcmd={} #tracks past commands that users have issued to prevent abuse
mostrecentnicks=[] #tracks most recent users sending commands

loop_count_for_updating_users=0
db={}
chansold={}
firstrun=True
msgqueue=[]
cached={}
keepRunning=True
lasterr=''
lastmsg=''
users_in_channel=[]

def lev(a,b):
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]
def closest(one,two):
	lowest=1000
	for o in one:
		for t in two:
			thisdist=lev(o,t)
			if thisdist < lowest and (thisdist <=1 or (thisdist <=3 and len(t) > 5) or (thisdist <=5 and len(t) > 7)):
				lowest=thisdist
	return lowest
db['config']=json.loads(sql.unique_get('data','config'))
db['config']['connect']['server']='127.0.0.1'
print 'entering loop'
while keepRunning:
	lines=[]
	if firstrun:
		firstrun=False
		readbuffer=""
		s=socket.socket( )
		s.connect((db['config']['connect']['server'], int(db['config']['connect']['port'])))
		print 'connected'
		s.send("NICK %s\r\n" % db['config']['connect']['username'])
		s.send("USER %s %s CFB :%s\r\n" % ("Football", "CFB", "College Football Robot"))
		print 'sent info'
		time.sleep(3)
		if not 'quit' in db['config']: db['config']['quit']=False
		s.send("PASS \r\n")
		s.setblocking(0)
		lastsent=time.time()
	try:
		db['config']['refresh']=True
		if db['config']['refresh']:
			cached={}
			db['config']['refresh']=False
		if not 'cfblive' in cached: cached['cfblive']=open('cfblive.py').read()
		exec cached['cfblive']
		if db['config']['quit'] == True:
			keepRunning=False
			db['config']['quit']=False
			s.send('quit :Quitting\r\n')
		time.sleep(.1)
	except:
		errr=traceback.format_exc()
		if str(errr) != lasterr: open('logs/error.log','a').write(str(errr)+'\r\n')
		lasterr=str(errr)
		if errr.lower().count('socket.error') != 0 or errr.lower().count('broken pip') != 0:
			s.close()
			keepRunning=False
