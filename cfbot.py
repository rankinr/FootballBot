import json, time, socket, string, random, time, os, hashlib, urllib, sys, traceback, HTMLParser, praw, urllib2
from HTMLParser import HTMLParser
import urlparse, re
from bs4 import BeautifulSoup
from mechanize import Browser
import oauth2 as oauth
import json, operator, math
import httplib
from xml.etree import ElementTree as etree

<<<<<<< HEAD
exec(open('/home/fbbot/cfb/sload.py').read()) # load mysql information
exec(open('/home/fbbot/cfb/common_functions.py')) #load custom functions
=======
exec (open('/home/fbbot/cfb/sload.py').read())

tmtype = 'PRIVMSG'
pastcmd = {}
cursedHoya = False
mostrecentnicks = []
msgs_flood = {}
quieted = []
this_loop = 0
last_loop = 0
ns_ping = [0, 0, 20, 0]  # last time, last time recorded, last value
>>>>>>> origin/master

announced=[] #to track games whose start has been announced
tmtype='PRIVMSG' # default message type is PRIVMSG
pastcmd={} #tracks past commands that users have issued to prevent abuse
mostrecentnicks=[] #tracks most recent users sending commands

<<<<<<< HEAD

db={}
chansold={}
firstrun=True
msgqueue=[]
cached={}
keepRunning=True
lasterr=''
lastmsg=''

def lev(a,b):
=======
def ctnums(ds):
    if re.search('[0-9]+', ds) != None:
        return len((re.search('[0-9]+', ds)).group())
    else:
        return 0


def surl(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url'
    postdata = {'longUrl': url}
    headers = {'Content-Type': 'application/json'}
    req = urllib2.Request(post_url, json.dumps(postdata), headers)
    ret = urllib2.urlopen(req).read()
    print ret
    return json.loads(ret)['id']


def sMsg(msg, l=400, split=','):
    if msg > l:
        msgs = []
        c = 0
        while len(msg) > l:
            c += 1
            msg1 = msg[:l][::-1]
            loc = len(msg1) - msg1.find(',')
            if c > 1: msgs.append("(cont'd) " + msg[:loc].strip())
            else: msgs.append(msg[:loc].strip())
            msg = msg[loc:].strip()
        if len(msg.strip()) > 0: msgs.append("(cont'd) " + msg.strip())
        return msgs
    else:
        return [msg]


def stats(gid):
    soup = BeautifulSoup(urllib.urlopen(
        'http://espn.go.com/college-football/matchup?gameId=' + gid).read(),
                         "html5lib")
    teams = soup.findAll('span', {'class': 'chartLabel'})
    t1 = teams[0].getText()
    t2 = teams[1].getText()
    tb = soup.find('article', {'class': 'team-stats-list'})
    tb = tb.find('table', {'class': 'mod-data'})
    rows = tb.findAll('tr')
    stats = []
    for row in rows:
        if row['class'][0] != 'header':
            cols = row.findAll('td')
            if len(cols) > 2:
                stats.append(cols[0].contents[0].strip(
                ) + ': ' + t1 + ' ' + cols[1].contents[0].strip() + ' ' + t2 +
                             ' ' + cols[2].contents[0].strip())
    return ', '.join(stats)
def gameInfo(gm,color=False,showMr=False,score=True,branked=False,custformat='',supershort=False):
    ourgame = db['games'][gm]
    if ourgame['status'].lower().count('pm et') != 0 or ourgame['status'].lower(
    ).count('am et') != 0:
        score = False
    t1c = ''
    t2c = ''
    if color:
        cis = artolower(db['colors'])
        if ourgame['team1'].lower() in cis:
            t1c = str(cis[ourgame['team1'].lower()][0]) + ',' + str(
                cis[ourgame['team1'].lower()][1])
        if ourgame['team2'].lower() in cis:
            t2c = str(cis[ourgame['team2'].lower()][0]) + ',' + str(
                cis[ourgame['team2'].lower()][1])
    t1s = ourgame['team1']
    t2s = ourgame['team2']
    if supershort: shorts = artolower(db['supershorten'])
    else: shorts = artolower(db['shorten'])
    if t1s.lower() in shorts and shorts[t1s.lower()].strip() != '':
        t1s = shorts[t1s.lower()]
    if t2s.lower() in shorts and shorts[t2s.lower()].strip() != '':
        t2s = shorts[t2s.lower()]
    if score:
        t1 = t1s + ' ' + ourgame['team1score']
        t2 = t2s + ' ' + ourgame['team2score']
    else:
        t1 = t1s
        t2 = t2s
    if len(t1.split()) > 1:
        if t1.split()[1][0] == '(': t1 = t1.split()[0]
    if len(t2.split()) > 1:
        if t2.split()[1][0] == '(': t2 = t2.split()[0]
    rks = artolower(db['ranks'])
    btgame = False
    #	print ourgame['team1'].lower()
    if ourgame['team1'].lower() in rks and rks[ourgame['team1'].lower()
                                           ] != None:
        t1 = '(' + rks[ourgame['team1'].lower()] + ') ' + t1
        #print branked
        if branked: btgame = True
    if ourgame['team2'].lower() in rks and rks[ourgame['team2'].lower()
                                           ] != None:
        t2 = '(' + rks[ourgame['team2'].lower()] + ') ' + t2
        if branked: btgame = True
    #print btgame
    ntwks = ''
    if gm in db['ntwks']:
        if db['ntwks'][gm] != '': ntwks = ' - ' + db['ntwks'][gm]
    mr = ''
    if ourgame['status'].upper().count('FINAL') == 1: ntwks = ''
    status = ourgame['status']
    if status.lower().count('am et') != 0 or status.lower().count('pm et') != 0:
        std = status
        stds = std[:std.find(',')]
        std = std[std.find(',') + 2:]
        std = std[std.find(' ') + 1:]
        std = std[std.find(' ') + 1:]
        std = stds + ' ' + std
        status = std
    status = status.replace(' ET', '') + ntwks
    poss = ''
    if ourgame['status'].upper().count(
            'FINAL') == 0 and ourgame['status'].upper().count(
                    'PM ET') == 0 and ourgame['status'].upper().count(
                            'AM ET') == 0 and showMr:
        mrg = mrsc(ourgame['gid'])
        poss = mrg[1]
        if showMr: mr = ': ' + mrg[0]
        if len(mr) < 5: mr = ''
    if t1c != '': t1 = chr(3) + t1c + t1 + chr(3)
    if t1c != '': t2 = chr(3) + t2c + t2 + chr(3)
    if ourgame['team1'] == poss: t1 = t1 + ' ' + chr(3) + '0,5<>' + chr(3)
    elif ourgame['team2'] == poss: t2 = t2 + ' ' + chr(3) + '0,5<>' + chr(3)
    nident = ' vs. '
    if 'neutral' in ourgame and not ourgame['neutral']: nident = ' @ '
    bt = ''
    if btgame: bt = '\x02'
    stat_to_show = ourgame['status'].strip()
    if supershort and (stat_to_show.count('PM ET') != 0 or
                           stat_to_show.count('AM ET') != 0):
        stat_to_show1 = stat_to_show[:stat_to_show.find(',')].strip()
        stat_to_show2 = stat_to_show[stat_to_show.find(',') + 1:].strip()
        stat_to_show2 = stat_to_show2[stat_to_show2.find(' '):].strip()
        stat_to_show2 = stat_to_show2[stat_to_show2.find(' '):].strip()
        stat_to_show = stat_to_show1 + ' ' + stat_to_show2
    if custformat != '':
        return custformat.replace('%BT%', bt.strip()).replace(
            '%T1%', t1.strip()).replace('%T2%', t2.strip()).replace(
                '%NIDENT%', nident.strip()).replace('%MR%', mr.strip()).replace(
                    '%STATUS%', stat_to_show.strip()).replace('%NTWKS%',
                                                              ntwks.strip())
    else:
        return bt + t1.strip() + nident + t2.strip() + '%ABOB%' + mr.strip(
        ) + ' ' + stat_to_show + ' ' + ntwks.strip() + bt
#			db['msgqueue'].append([t1+' '+nident+t2.strip()+mr.strip()+' '+ourgame['status']+ntwks,dest,tmtype,'score'])


def k4v(v, ar):
    for a, b in ar.iteritems():
        if b == v:
            return a


def mrsc(gid):
    pg = urllib.urlopen("http://espn.go.com/ncf/playbyplay?gameId=" + gid).read(
    )
    pg = pg[pg.find('espn.gamepackage.data = ') + len(
        'espn.gamepackage.data = '):]
    pg = pg[:pg.find('}};') + 2]
    pg = json.loads(pg)
    try:
        poss = k4v(pg['drives']['current']['plays'][0]['end']['team']['id'],
                   db['teams'])
        toret = pg['drives']['current']['plays'][-1][
            'text'
        ] + ' (This drive: ' + pg['drives']['current']['description'] + ')'
        return [toret, poss]
    except:
        return ['', '']


def abbrev(words, abb, debug=False):
    debug = False
    con = abb
    for throw, ws in con.iteritems():
        #print words.lower()+'.'+ws[0].lower()+'.'
        if words.lower().strip() == ws[0].lower().strip(): words = ws[1]
        if debug: print words + '.' + ws[0] + '.' + ws[1] + '.'
    return words


def match(w):
    closestval = 1000000
    closests = ''
    teams = db['games']
    params = abbrev(w.lower(), db['abbreviations'], True)
    for a, b in teams.iteritems():
        if a != 'lastupdate':
            team1 = b['team1'].lower().replace('(', '').replace(')', '')
            team2 = b['team2'].lower().replace('(', '').replace(')', '')
            tclv1 = closest([params, params + ' StateZ'], [team1])
            tclv2 = closest([params, params + ' StateZ'], [team2])
            if tclv1 < closestval:
                closestval = tclv1
                closests = team1
            if tclv2 < closestval:
                closestval = tclv2
                closests = team2
    if closests != '' and closestval < 3:
        return closests
    else:
        return False


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


db = {}
chansold = {}
firstrun = True
msgqueue = []
cached = {}
keepRunning = True
lasterr = ''
lastmsg = ''


def artolower(art):
    newar = {}
    for a, b in art.iteritems():
        newar[a.lower()] = b
    return newar


def lev(a, b):
>>>>>>> origin/master
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]


def closest(one, two):
    lowest = 1000
    for o in one:
        for t in two:
            thisdist = lev(o, t)
            if thisdist < lowest and (thisdist <= 1 or
                                      (thisdist <= 3 and len(t) > 5) or
                                      (thisdist <= 5 and len(t) > 7)):
                lowest = thisdist
    return lowest


db['config'] = json.loads(sql.unique_get('data', 'config'))
db['config']['connect']['server'] = '127.0.0.1'
print 'entering loop'
while keepRunning:
<<<<<<< HEAD
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
=======
    lines = []
    if firstrun:
        firstrun = False
        readbuffer = ""
        s = socket.socket()
        s.connect((db['config']['connect']['server'], int(
            db['config']['connect']['port'])))
        print 'connected'
        s.send("NICK %s\r\n" % db['config']['connect']['username'])
        s.send("USER %s %s CFB :%s\r\n" %
               ("Football", "CFB", "College Football Robot"))
        print 'sent info'
        time.sleep(3)
        if not 'quit' in db['config']: db['config']['quit'] = False
        s.send("PASS \r\n")
        s.setblocking(0)
        lastsent = time.time()
    try:
        db['config']['refresh'] = True
        if db['config']['refresh']:
            cached = {}
            db['config']['refresh'] = False
        if not 'cfblive' in cached:
            cached['cfblive'] = open('cfblive.py').read()
        exec cached['cfblive']
        if db['config']['quit'] == True:
            keepRunning = False
            db['config']['quit'] = False
            s.send('quit :Quitting\r\n')
        time.sleep(.1)
    except:
        errr = traceback.format_exc()
        if str(errr) != lasterr:
            open('logs/error.log', 'a').write(str(errr) + '\r\n')
        lasterr = str(errr)
        if errr.lower().count('socket.error') != 0:
            s.close()
            keepRunning = False
>>>>>>> origin/master
