import urllib
def stats(gid):
	retar=[]
	info=urllib.urlopen('http://espn.go.com/ncf/recap?gameId='+str(gid)).read()
	info=info[info.find("Team Stat Comparison"):info.find('<h4>Passing Leaders</h4>')]
	info=info[info.find(' floatleft" style="margin-right: 6px;"></div>')+len(' floatleft" style="margin-right: 6px;"></div>'):]
	team1=info[:info.find('</th>')]
	info=info[info.find(' floatleft" style="margin-right: 6px;"></div>')+len(' floatleft" style="margin-right: 6px;"></div>'):]
	team2=info[:info.find('</th>')]
	while info.count('<td class="bi" style="text-align:left;">') != 0:
		info=info[info.find('<td class="bi" style="text-align:left;">')+len('<td class="bi" style="text-align:left;">'):]
		stype=info[:info.find('</td')]
		info=info[info.find('<td>')+len('<td>'):]
		t1=info[:info.find('</td>')]
		t2=info[info.find('<td>')+len('<td>'):]
		t2=t2[:t2.find('</td>')]
		retar.append((stype+': '+team1+' '+t1+'-'+team2+' '+t2).strip())
	return retar
print len(', '.join(stats(332572483)))
