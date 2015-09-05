import re, urllib, os, fcntl, json, urlparse, re, random, time
from BeautifulSoup import BeautifulSoup
from mechanize import Browser


def mrsc(gid):
    mech = Browser()
    url = "http://espn.go.com/ncf/playbyplay?gameId=" + gid + "&period=0"
    #print url
    page = mech.open(url)
    html = page.read()
    print url
    if html.count('Play-by-play not currently available.') == 0:
        soup = BeautifulSoup(html)
        table = soup.findAll("table")[-1]
        rows = table.findAll('tr')[::-1]
        c = 0
        toret = ''
        keepgoing = True
        cup = html[::-1][:html[::-1].find(
            ' left; font: 700 14px/25px Helvetica,Arial,sans-serif;" colspan="3"><div style="margin-right: 6px;"' [::
                                                                                                                   -
                                                                                                                   1])][::
                                                                                                                        -
                                                                                                                        1]
        cup = cup[cup.find('a name="') + len('a name="'):]
        cup = cup[:cup.find('"')]
        while c < 7 and keepgoing and c < len(rows):
            cols = rows[c].findAll('td')
            #print rows[c]
            if len(cols) > 2:
                #if str(cols[2]) != '<td>&nbsp;</td>' and str(cols[3]) != '<td>&nbsp;</td>':
                toret = str(' '.join(cols[0].findAll(text=True))) + '. ' + str(
                    ' '.join(cols[1].findAll(text=True)))
                keepgoing = False
            c = c + 1
        toret = toret.replace('  ', ' ').strip()
        if toret != '': toret = toret + ' '
        poss = ''
        if cup != '' and len(cup) < 30: poss = cup
    else:
        toret = ''
        poss = ''
    return [toret, poss]


st = time.time()
c = 0
keepGoing = True
while time.time() < st + 60 * 4.65 and keepGoing:
    fdb = open('/home/fbbot/cfb/db.json', 'r')
    fcntl.flock(fdb, fcntl.LOCK_EX)
    db = json.load(fdb)
    if not 'followingrecent' in db: db['followingrecent'] = {}
    following = db['following']
    open('/home/fbbot/cfb/db.json', 'w').write(json.dumps(db))
    fcntl.flock(fdb, fcntl.LOCK_UN)
    msgqueue = []
    loopc = 0
    for a, b in following.iteritems():
        if a in db['games'] and len(b) != 0 and db['games'][a]['status'].lower(
        ).count('final') == 0 and db['games'][a]['status'].lower(
        ).count('am est') == 0 and db['games'][a]['status'].lower().count(
                'pm est') == 0 and db['games'][a]['status'].lower().count(
                        'halftime') == 0:
            loopc += 1
            print 'Loading ' + a
            tg = mrsc(db['games'][a]['gid'])
            if not a in db['followingrecent']: db['followingrecent'][a] = ''
            ourgame = db['games'][a]
            nident = ' vs. '
            if 'neutral' in ourgame:
                if not ourgame['neutral']: nident = ' @ '
            t1 = ourgame['team1']
            t2 = ourgame['team2']
            if t1 == tg[1]: t1 = '\x02' + t1 + '\x02'
            elif t2 == tg[1]: t2 = '\x02' + t2 + '\x02'
            #print tg[0]
            if len(tg[0].strip(
            )) != 0 and db['followingrecent'][a] != t1 + ' ' + ourgame[
                    'team1score'
            ] + nident + t2 + ' ' + ourgame['team2score'] + ': ' + tg[0]:
                msgqueue.append([t1 + ' ' + ourgame['team1score'
                                   ] + nident + t2 + ' ' + ourgame['team2score']
                                 + ': ' + tg[0], a, ourgame['status']])
        if loopc == 0: keepGoing = False
    fdb = open('/home/fbbot/cfb/db.json', 'r')
    fcntl.flock(fdb, fcntl.LOCK_EX)
    db = json.load(fdb)
    for a in msgqueue:
        for b in db['following'][a[1]]:
            db['msgqueue'].append([a[0] + ' (' + a[2] + ')', b])
            #print 'sent to '+b+': '+a[0]
        db['followingrecent'][a[1]] = a[0]
    #print db['msgqueue']
    open('/home/fbbot/cfb/db.json', 'w').write(json.dumps(db))
    fcntl.flock(fdb, fcntl.LOCK_UN)
    time.sleep(random.randrange(15, 25))
