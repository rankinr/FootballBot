import urllib,json, urllib2
from oauth2client.client import flow_from_clientsecrets
from bs4 import BeautifulSoup
exec(open('/home/fbbot/cfb/sload.py').read())
exec(open('/home/fbbot/cfb/common_functions.py').read())
sbnation=BeautifulSoup(urllib.urlopen('http://www.sbnation.com/college-football'),"html5lib")
articles=sbnation.findAll('a',{'data-native-ad-id':'headline'})
old_news=open('/home/fbbot/cfb/updaters/loaded_news').read().split('\n')
new_news=[]
db={}
for article in articles:
	news_p=article.contents[0]+' '+article['href']
	news_a=article.contents[0]+' *'+shorten_url(article['href'])+'*'
	if not news_p in old_news and not article.contents[0] in old_news and not article['href'] in old_news: 
		new_news.append(news_a)
		open('/home/fbbot/cfb/updaters/loaded_news','a').write(news_p+'\n'+article['href']+'\n'+article.contents[0]+'\n')
	#print article
if len(new_news) != 0:
	db['colors']=artolower(json.loads(sql.unique_get('data','colors')))
	db['abbreviations']=json.loads(sql.unique_get('data','abbreviations'))
	abbrev_lower={}
	for b,a in db['abbreviations'].iteritems():
		abbrev_lower[a[0].lower().replace(' ','')]=a[1]
	db['msgqueue']=json.loads(sql.unique_get('data','msgqueue'))
	for news_art in new_news:
		news_art=news_art.split(' ')
		last_word=''
		last_word2=''
		last_news_art_1=news_art
		last_news_art_2=news_art
		last_news_art_3=news_art
		for word in news_art:
			new_word=word
			new_last_word=last_word
			new_last_word2=last_word2
			if new_word.count("'") != 0: new_word=new_word[:new_word.find("'")]
			#if new_word.lower() in abbrev_lower: new_word=abbrev_lower[word.lower()]
			new_word=new_word.lower()
			if new_last_word.count("'") != 0: new_last_word=new_last_word[:new_last_word.find("'")]
			#if new_last_word.lower() in abbrev_lower: new_last_word=abbrev_lower[last_word.lower()]
			if new_last_word2.count("'") != 0: new_last_word2=new_last_word2[:new_last_word2.find("'")]
			#if new_last_word2.lower() in abbrev_lower: new_last_word2=abbrev_lower[last_word2.lower()]
			new_word=new_word.lower()
			new_last_word=new_last_word.lower()
			new_last_word2=new_last_word2.lower()
			#print news_art
			#print '.'+new_last_word2+' '+new_last_word+' '+new_word+'.'
			"""if new_last_word2+' '+new_last_word+' '+new_word in db['colors']: 
				news_art=last_news_art_3
				print news_art
				news_art[news_art.index(last_word2)]=chr(3)+str(db['colors'][new_last_word2+' '+new_last_word+' '+new_word][0])+','+str(db['colors'][new_last_word2+' '+new_last_word+' '+new_word][1])+last_word2
				news_art[news_art.index(word)]=word+chr(3)
			elif new_last_word+' '+new_word in db['colors']: 
				news_art=last_news_art_1
				news_art[news_art.index(new_last_word+' '+new_word)]=chr(3)+str(db['colors'][new_last_word+' '+new_word][0])+','+str(db['colors'][new_last_word+' '+new_word][1])+last_word
				news_art[news_art.index(word)]=word+chr(3)"""
			#if new_word in db['colors']: news_art[news_art.index(word)]=chr(3)+str(db['colors'][new_word][0])+','+str(db['colors'][new_word][1])+word+chr(3)
			last_news_art_3=last_news_art_2[:]
			last_news_art_2=last_news_art_1[:]
			last_news_art_1=news_art[:]
			last_word2=last_word
			last_word=word
		news_art=' '.join(news_art)
		db['msgqueue'].append([news_art,None,None,'score',False])
		#db['msgqueue'].append([news_art,'#cfbtest',None,False])
	print db['msgqueue']
	sql.unique_set('data','msgqueue',json.dumps(db['msgqueue']))