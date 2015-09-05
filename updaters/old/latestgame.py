import mechanize, cookielib, time, socket, sys, string, random, time, json
exec open('/home/rob/cfb/fxns/writefxn.py').read()
teams = json.load(open('/home/rob/cfb/.db.json'))


def openpage(linkk):
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [(
        'User-agent',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
    )]
    return br.open(linkk).read()


def getlatest(gameid):
    z = openpage('http://espn.go.com/ncf/playbyplay?gameId=' + gameid +
                 '&period=0')
    if z.count(
        "<script type='text/javascript'> //<![CDATA[ (function(){ window.gravityInsightsParams = { 'type': 'content', 'action': '', 'site_guid': '9a41401e9b7c945344e001ee7f23031e' };") != 0:
        z = ''
    z = z[:z.find(
        '<td>&nbsp;</td><td>&nbsp;</td></tr></tbody></table></div></div>')]
    z = z[z.find('<td colspan="2"'):]
    curarray = []
    cz = 0
    while z != '':
        cz = cz + 1
        if cz > 10000: z = ''
        z = z[z.find('<td colspan="2"') + len('<td colspan="2"'):]
        z = z[z.find('<td'):]
        z = z[z.find('>') + 1:]
        cur = z[:z.find('</td>')]
        cc = 0
        while cur.count('<') != 0:
            cc = cc + 1
            if cc > 50: cur = ''
            if cur.find('<') < cur.find('>'):
                first = '<'
                last = '>'
            else:
                first = '>'
                last = '<'
            cur1 = cur[:cur.find(first)]
            cur2 = cur[cur.find(last) + 1:]
            cur = cur1 + cur2
        cur = cur.replace('&nbsp', ' ')
        cur = cur.replace('\t', ' ')
        while cur.count('  ') != 0:
            cur = cur.replace('  ', ' ')
        cur = cur.replace('\r', '')
        cur = cur.replace('\n', '')
        if len(cur) > 5: curarray.append(cur)
    if len(curarray) != 0: return curarray[-1]
    else: return False


lastmsg = open('/home/rob/cfb/.last_latestgame').read()
c = 0
while c < 4:
    time.sleep(random.randrange(10, 20))
    tg = '332570245'
    curmsg = getlatest(tg)
    print curmsg
    if curmsg != lastmsg:
        mqa([curmsg, '#cfbtest'])
        lastmsg = curmsg
        open('/home/rob/cfb/.last_latestgame', 'w').write(lastmsg)
    c += 1
#game-status final
