"""Looks up games by team name ("!score UMiami"), conference ("!score ACC") or time ("!score 330").
"score" can be omitted (i.e., "!UMiami", "!ACC", or "!330" will produce the same results as above)
"""


def mrsc(gid):
    pg = urllib.urlopen("http://espn.go.com/ncf/playbyplay?gameId=" + gid).read(
    )
    pg = pg[pg.find('espn.gamepackage.data = ') + len(
        'espn.gamepackage.data = '):]
    pg = pg[:pg.find('}};') + 2]
    try:
        pg = json.loads(pg)
        poss = k4v(pg['drives']['current']['plays'][0]['end']['team']['id'],
                   db['teams'])
        toret = pg['drives']['current']['plays'][-1][
            'text'
        ] + ', ' + pg['drives']['current']['plays'][-1]['end'][
            'downDistanceText'
        ] + ' (This drive: ' + pg['drives']['current']['description'] + ')'
        return [toret, poss]
    except:
        return ['', '']


def abbrev(words, abb, debug=False):
    con = abb
    print words
    for throw, ws in con.iteritems():
        #print words.lower()+'.'+ws[0].lower()+'.'
        if ws[0] != None and words.lower().strip() == ws[0].lower().strip():
            words = ws[1]
        #if debug: print words+'.'+ws[0]+'.'+ws[1]+'.'
    return words
def gameInfo(gm,color=False,showMr=False,score=True,branked=False,custformat='',supershort=False,newdb=False):
    if not newdb: ourgame = db['games'][gm]
    else: ourgame = newdb[gm]
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
    if ourgame['team1'] == poss: t1 = t1 + ' (:)'
    elif ourgame['team2'] == poss: t2 = t2 + ' (:)'
    if t1c != '': t1 = chr(3) + t1c + t1 + chr(3)
    if t2c != '': t2 = chr(3) + t2c + t2 + chr(3)
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
        return bt + t1.strip() + nident + t2.strip() + mr.strip(
        ) + ' ' + stat_to_show + ' ' + ntwks.strip() + bt
#			db['msgqueue'].append([t1+' '+nident+t2.strip()+mr.strip()+' '+ourgame['status']+ntwks,dest,tmtype,'score'])

un_team = False
newo = ''

if (origin.count('|') != 0 or origin.count('[') != 0):
    if origin.count('|') != 0: newo = origin[origin.find('|') + 1:]
    elif origin.count('[') != 0:
        newo = origin[origin.find('[') + 1:]
        if newo.count(']') != 0: newo = newo[:newo.find(']')]
    if ''.join(params).strip() == '' and newo.strip() != '':
        params = [newo.strip()]
    if newo.strip() != '': un_team = match(newo)


def surl(url):
    try:
        post_url = 'https://www.googleapis.com/urlshortener/v1/url'
        postdata = {'longUrl': url}
        headers = {'Content-Type': 'application/json'}
        req = urllib2.Request(post_url, json.dumps(postdata), headers)
        ret = urllib2.urlopen(req).read()
        #print ret
        return json.loads(ret)['id']
    except:
        return ''


if ''.join(params).strip() != '':
    tbyname = {}
    closestval = 1000000
    closests = ''
    teams = db['games']
    params = abbrev(' '.join(params).lower(), db['abbreviations'])
    for a, b in teams.iteritems():
        if a != 'lastupdate':
            team1 = b['team1'].lower().replace('(', '').replace(')', '')
            team2 = b['team2'].lower().replace('(', '').replace(')', '')
            if params.count(' ') == 0:
                tclv = closest([params.lower(), params.lower() + ' StateZ',
                                params.lower().replace('st', 'state')],
                               [team1.lower(), team2.lower()])
            else:
                tclv = closest([params.lower(), params.lower().replace(
                    'st', 'state')], [team1.lower(), team2.lower(),
                                      team1.lower() + team2.lower(),
                                      team2.lower() + team1.lower()])
            if tclv < closestval:
                closestval = tclv
                closests = a
    if dest == 'footballbot' or dest == 'footballtestbot': dest = origin

    if closests != '' and closestval <= 3:
        db['msgqueue'].append([gameInfo(closests, True, True) + '*PR* ' + surl(
            'http://sports.espn.go.com/ncf/boxscore?gameId=' +
            teams[closests]['gid']) + '*PR*', dest, tmtype, 'score'])
    else:
        conf = []
        closest_conf = ''
        closest_conf_val = 100000
        db['conferences'] = json.loads(sql.unique_get('data', 'conferences'))
        for a, b in db['conferences'].iteritems():
            clv_conf = closest([params.lower()], [a.lower()])
            if clv_conf < closest_conf_val:
                closest_conf_val = clv_conf
                closest_conf = a
        #db['msgqueue'].append([closest_conf+str(closest_conf_val),'harkatmuld','PRIVMSG'])
        if closest_conf != '' and closest_conf_val <= 3:
            #closest_conf_val
            for c in db['conferences'][closest_conf]:
                for a, b in teams.iteritems():
                    if a != 'lastupdate':
                        #return bt+t1.strip()+nident+t2.strip()+mr.strip()+' '+status+bt
                        #gm,color=False,showMr=False,score=True,branked=False,custformat='
                        if c.lower() == b['team1'].lower() or c.lower(
                        ) == b['team2'].lower():
                            ta = gameInfo(
                                a, True, False, True, False,
                                '%BT%%T1% %NIDENT% %T2% %MR%%STATUS%%BT%',
                                True).replace(' IN ', ' ').replace(
                                    'vs.',
                                    'v').replace('HALFTIME', 'HALF').replace(
                                        ' ET', '').replace(' PM', 'PM').replace(
                                            ' AM', 'AM')
                            if not ta in conf: conf.append(ta)
        conf = ', '.join(conf)
        conf = conf.strip()
        if len(conf) < 10: conf = ''
        if conf != '':
            db['msgqueue'].append([conf, dest, 'PRIVMSG', None])
        else:
            if ''.join(params).lower().replace(' ', '') == 'top25':
                topar = []
                for a, b in db['games'].iteritems():
                    if a != 'lastupdate':
                        t1rk = 26
                        t2rk = 26
                        rks = artolower(db['ranks'])
                        if b['team1'].lower() in rks:
                            t1rk = rks[b['team1'].lower()]
                        if b['team2'].lower() in rks:
                            t2rk = rks[b['team2'].lower()]
                        if t1rk == None: t1rk = 26
                        if t2rk == None: t2rk = 26
                        #print b['team1']+' '+str(t1rk)+' '+b['team2']+' '+str(t2rk)
                        trk = 26
                        #print t1rk
                        if int(t1rk) <= 25 or int(t2rk) <= 25:
                            if int(t1rk) < int(t2rk): trk = t1rk
                            else: trk = t2rk
                            topar.append({'game': a, 'rk': int(trk)})
                #print 'topar:'
                #print  topar
                topar = sorted(topar, key=lambda k: k['rk'])
                #print topar
                topar2 = []
                topvals = ''
                for a in topar:
                    topar2.append(gameInfo(
                        a['game'], True, False, True, False,
                        '%BT%%T1% %NIDENT% %T2% %MR%%STATUS%%BT%',
                        True).replace(' IN ', ' ').replace('vs.', 'v').replace(
                            'HALFTIME', 'HALF').replace(' ET', '').replace(
                                ' PM', '').replace(' AM', ''))
                topvals = ', '.join(topar2)
                #print 'tops:'+topvals
                db['msgqueue'].append([topvals, dest, 'PRIVMSG', None])
            else:

                fcs = json.loads(sql.unique_get('data', 'fcs'))
                closests = ''
                closestval = 100
                for aa, bb in fcs.iteritems():
                    if aa != 'lastupdate':
                        team1 = bb['team1'].lower().replace('(', '').replace(
                            ')', '')
                        team2 = bb['team2'].lower().replace('(', '').replace(
                            ')', '')
                        if params.count(' ') == 0:
                            tclv = closest(
                                [params.lower(), params.lower() + ' StateZ',
                                 params.lower().replace('st', 'state')],
                                [team1.lower(), team2.lower()])
                        else:
                            tclv = closest(
                                [params.lower(), params.lower().replace('st',
                                                                        'state')
                         ], [team1.lower(), team2.lower(), team1.lower() +
                             team2.lower(), team2.lower() + team1.lower()])
                        if tclv < closestval:
                            closestval = tclv
                            closests = aa
                if dest == 'footballbot' or dest == 'footballtestbot':
                    dest = origin

                if closests != '' and closestval <= 3:
                    db['msgqueue'].append(
                        [gameInfo(closests,
                                  True,
                                  True,
                                  newdb=fcs) + '*PR* ' +
                         surl('http://sports.espn.go.com/ncf/boxscore?gameId=' +
                              fcs[closests]['gid']) + '*PR*', dest, tmtype,
                         'score'])

                else:
                    clv_isteam_val = 100000
                    clv_isteam_act = ''
                    for a, b in db['colors'].iteritems():
                        clv_isteam = closest([params.lower(), params.replace(
                            'st', 'state').lower()], [a.lower()])
                        if clv_isteam < clv_isteam_val:
                            clv_isteam_val = clv_isteam
                            clv_isteam_act = a
                    if clv_isteam_val <= 3:
                        db['msgqueue'].append(
                            [origin + ': ' + clv_isteam_act +
                             ' has a bye week (or is not a FBS team).', dest,
                             'PRIVMSG', None])
                    else:
                        numbers = re.compile('\d+(?:\.\d+)?')
                        pnum = ''.join(numbers.findall(params))
                        pnum = pnum
                        pnum = pnum[:-2] + ':' + pnum[-2:]
                        if len(pnum) == 4 or len(pnum) == 5:
                            conf = []
                            for a, b in teams.iteritems():
                                if a != 'lastupdate':
                                    #return bt+t1.strip()+nident+t2.strip()+mr.strip()+' '+status+bt
                                    #gm,color=False,showMr=False,score=True,branked=False,custformat='
                                    if b['status'].count(
                                            pnum) != 0 and b['status'].count(
                                                    'ET') != 0:
                                        ta = gameInfo(
                                            a, True, False, True, False,
                                            '%BT%%T1% %NIDENT% %T2% %MR% %NTWKS%%BT%',
                                            True).replace(' IN ', ' ').replace(
                                                'vs.', 'v').replace(
                                                    'HALFTIME', 'HALF').replace(
                                                        ' ET', '').replace(
                                                            ' PM',
                                                            'PM').replace(' AM',
                                                                          'AM')
                                        if not ta in conf:
                                            conf.append(ta.strip())
                            conf = ', '.join(conf)
                            conf = conf.strip()
                            if len(conf) < 10: conf = ''
                            if conf != '':
                                db['msgqueue'].append([conf, dest, 'PRIVMSG',
                                                       None])
                            else:
                                db['msgqueue'].append(
                                    [origin +
                                     ': I can\'t find any games starting at ' +
                                     pnum + '.', dest, 'PRIVMSG', None])

                        else:
                            db['msgqueue'].append([
                                origin +
                                ': I do not know what team you are referring to.',
                                dest, 'PRIVMSG', None
                            ])
        #[msg,channel (all main chans), type(privmsg),identifier(None)]
