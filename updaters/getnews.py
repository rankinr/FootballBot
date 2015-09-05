import re, urllib, os, fcntl, json
fdb = open('/home/fbbot/cfb/db.json', 'r')
fcntl.flock(fdb, fcntl.LOCK_EX)
db = json.load(fdb)

#pattern=re.compile('[\W_]+')
z = urllib.urlopen('http://sports.espn.go.com/espn/rss/ncf/news').read()


def tinyurl(url):
    return urllib.urlopen("http://tinyurl.com/api-create.php?url=" + url).read()


title = re.compile('<title><!\[CDATA\[(.*)\]\]></title>')
link = re.compile('<guid isPermaLink="false">(.*)</guid>')
find_title = re.findall(title, z)
find_link = re.findall(link, z)
oldnews = db['oldnews']
c = 0
for title in find_title:
    title = title.replace('\r', '').replace('\n', '')
    if oldnews.count(title) == 0:
        db['oldnews'].append(title)
        db['msgqueue'].append([title.strip() + ':' + chr(3) + ' ' + tinyurl(
            find_link[c]), None, None, 'news'])
    c += 1
while len(db['oldnews']) > 30:
    db['oldnews'].pop(0)
open('/home/fbbot/cfb/db.json', 'w').write(json.dumps(db))
fcntl.flock(fdb, fcntl.LOCK_UN)
