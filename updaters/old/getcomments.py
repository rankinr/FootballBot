import urllib2, re, string, urllib, time, unicodedata
urllib.urlcleanup()
exec open('/home/rob/cfb/fxns/writefxn.py')
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'robs reddit irc robot')]
ourlisting = json.loads(opener.open(
    'http://www.reddit.com/r/CFB/search.json?q=title%3AGame+Thread&restrict_sr=on&t=day&sort=top').read(
    ))
#ourlisting=json.load(open('savebw'))
gtr = re.compile(re.escape('game thread'), re.IGNORECASE)
ourlisting['data']['children'] = ourlisting['data']['children'][:7]
for id in ourlisting['data']['children']:
    score = id['data']['score']
    title = id['data']['title']
    title = re.sub(r'\([^)]*\)', '', gtr.sub('', title.replace('[', '').replace(
        ']', ''))).strip()
    url = id['data']['url']
    if score > 5:
        cmts = json.loads(opener.open(url + '.json?sort=new&throw=' + str(
            time.time())).read())[1]['data']['children']
        for cmt in cmts:
            isMain = True
            try:
                wur = cmt['data']['body']
            except:
                isMain = False
            if isMain:
                thiscmt = cmt['data']['body']
                thiscmt = unicodedata.normalize('NFKD', thiscmt).encode(
                    'ascii', 'ignore')
                thiscmt = str(thiscmt[:150]).replace('\r', ' ').replace(
                    '\n', ' ').replace('\t', ' ').replace('\x0b', ' ').replace(
                        '\x0c', ' ').replace(':', '')
                while thiscmt.count('  ') != 0:
                    thiscmt = thiscmt.replace('  ', ' ')
                if len(cmt['data']['body']) > 150:
                    thiscmt = thiscmt[::-1][thiscmt[::-1].find(" "):][::-1
                                                    ] + '...'
                thiscmt = thiscmt.strip()
                cscore = cmt['data']['ups'] - cmt['data']['downs']
                created = cmt['data']['created_utc']
                if cscore > 5:
                    scoreval = cscore / ((time.time() - created) / 60)
                else:
                    scoreval = 0
                oldcmts = open('/home/rob/cfb/.oldcmts').read()
                if scoreval > 1: print thiscmt + ' (' + str(scoreval) + ')'
                if scoreval > 6 and oldcmts.count(':' + cmt['data']['id'] +
                                                      ':') == 0:
                    #[msg,channel (all main chans), type(privmsg),identifier(None)]
                    mqa(['"' + thiscmt + '" -' + cmt['data']['author'] + ' (' +
                         title + ')', None, None, 'comment'])
                    open('/home/rob/cfb/.oldcmts',
                         'a').write(':' + cmt['data']['id'] + ':')
            #cmtsar.append([thiscmt,cscore,cmt['data']['id'],title,cmt['data']['author']])
            #print title+str(score)
"""if len(cmtsscores) != 0:
	if len(cmtsscores) < 10: minval=sorted(cmtsscores)[::-1][-1]
	else: minval=sorted(cmtsscores)[::-1][9]
	oldcmts=open('/home/rob/cfb/.oldcmts').read()
	for cmt in cmtsar:
		if cmt[1] >= minval and oldcmts.count(':'+cmt[2]+':') == 0:
			open('/home/rob/cfb/.oldcmts','a').write(':'+cmt[2]+':')
			mqa('"'+cmt[0]+'" -'+cmt[4]+' ('+cmt[3]+')')"""
