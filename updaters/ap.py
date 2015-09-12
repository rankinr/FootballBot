import re, urllib, os, fcntl, json, time
c = 0


def tinyurl(url):
    return urllib.urlopen("http://tinyurl.com/api-create.php?url=" + url).read()


keeploop = True
while keeploop:
    c += 1
    if c > 14: keeploop = False
    else:
        z = urllib.urlopen('http://collegefootball.ap.org/poll/2013/' + str(
            c)).read()
        if z.count('The page you are looking for is no longer here.') == 1:
            keeploop = False
if c <= 14:
    turl = tinyurl('http://collegefootball.ap.org/poll/2013/' + str(c))
    loopc = 0
    keepgoing = True
    os.system('clear')
    print 'Checking for week ' + str(c) + ' poll release.'
    while loopc < 3600 * 3 / 15 and keepgoing:
        z = urllib.urlopen('http://collegefootball.ap.org/poll/2013/' + str(
            c)).read()
        if z.count('The page you are looking for is no longer here.') == 0:
            keepgoing = False
            fdb = open('/home/fbbot/cfb/db.json', 'r')
            fcntl.flock(fdb, fcntl.LOCK_EX)
            try:
                db = json.load(fdb)
                db['msgqueue'].append(['The Week ' + str(
                    c) + ' AP Poll has been released: ' + turl, None, None,
                                       'score'])
                open('/home/fbbot/cfb/db.json', 'w').write(json.dumps(db))
                fcntl.flock(fdb, fcntl.LOCK_UN)
            except:
                fcntl.flock(fdb, fcntl.LOCK_UN)
        time.sleep(15)
        loopc += 1
