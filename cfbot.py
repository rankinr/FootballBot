import json,time,socket,string,random,time,os,hashlib,urllib,sys,traceback,HTMLParser,praw,urllib2
from HTMLParser import HTMLParser
import urlparse,re
from bs4 import BeautifulSoup
from mechanize import Browser
import oauth2 as oauth
import json, operator, math
import httplib
from xml.etree import ElementTree as etree
prefix=str(sys.argv)
if len(sys.argv) == 1: 
	prefix=''
	prefix_un=''
else: 
	prefix=str(sys.argv[1])+'_'
	prefix_un='_'+str(sys.argv[1])
exec(open('/home/fbbot/cfb/sload.py').read()) # load mysql information
exec(open('/home/fbbot/cfb/common_functions.py')) #load custom functions
os.system('ls -lah /home/fbbot/cfb/live_modules/ > .live_modules_dir')
live_modules=open('/home/fbbot/cfb/.live_modules_dir').read().split('\n')
announced=[] #to track games whose start has been announced
tmtype='PRIVMSG' # default message type is PRIVMSG
pastcmd={} #tracks past commands that users have issued to prevent abuse
mostrecentnicks=[] #tracks most recent users sending commands
sentMass=True
users_online=[]
last_users_update=0
mods_list=[]
new_users_online=[]
games_nextloop=[]
last_msgs={}

rcfb_msgs=[]
user_messages={}
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
lasterrl=''
isAutoDetect=False
lastAutoDetect=''
lastAutoDetectTime=time.time()
irc_flairs_new=json.loads(urllib.urlopen('http://162.243.6.111:7778/kiwi/assets/libs/final.json').read())
last_alert=time.time()

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
db['config']=json.loads(sql.unique_get('data','config'))
db['conferences']=json.loads(sql.unique_get('data','conferences'))
db['abbreviations']=json.loads(sql.unique_get('data','abbreviations'))
db['config']['connect']['server']='127.0.0.1'
conf_lower=[]
for a,b in db['conferences'].iteritems():
	conf_lower.append(a.lower().replace(' ',''))
abbrev_lower={}
for b,a in db['abbreviations'].iteritems():
	abbrev_lower[a[0].lower().replace(' ','')]=a[1]
print 'entering loop'
while keepRunning:
	lines=[]
	if firstrun:
		firstrun=False
		readbuffer=""
		s=socket.socket( )
		s.connect((db['config']['connect']['server'], int(db['config']['connect']['port'])))
#		s.connect(('morgan.freenode.net', 6667))
		print 'connected'
		s.send("NICK %s\r\n" % db['config']['connect']['username'])
		s.send("USER %s %s CFB :%s\r\n" % ("Football", "CFB", "College Football Robot"))
		print 'sent info'
		time.sleep(3)
		if not 'quit' in db['config']: db['config']['quit']=False
		s.send("PASS FootballBot"+prefix_un+":\r\n")
		s.setblocking(0)
		lastsent=time.time()
	try:
		print 'loop'
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
		if str(errr) != lasterr: 
			open('logs/error.log','a').write(str(errr)+'\r\n')
			errd=str(errr)
			errd=errd[errd.find(':')+1:].replace('\n',' ').replace('\r','').strip()
			#s.send('PRIVMSG #cfbtest : harkatmuld, there is an error: '+errd)
		errors=json.loads(sql.unique_get('data','errors'))
		if errr in errors: errors[errr][0]+=1
		else: errors[errr]=[1,0]
		errors[errr][1]=time.time()
		print json.dumps(errors)
		sql.unique_set('data','errors',json.dumps(errors))
		lasterr=str(errr)
		if errr.lower().count('socket.error') != 0 or errr.lower().count('broken pip') != 0:
			s.close()
			keepRunning=False
