"""Returns most popular comments in <Team>'s Game Thread in the past <Minutes> minutes. (Minutes defaults to 1 and is limited by the number of comments reddit will return-usually that means 5-10 minutes.)
Usage: !thread <Team> <Minutes> | Example: !thread Georgia Tech 4"""
game=params
try:
	mins=int(params[-1])
	game=params[:-1]
except: mins=1
secs=mins*60
#MATCHING CODE - MAYBE YOU SHOULD PUT THIS IN A FUNCTION
	
closestval=1000000
closests=''
teams=db['games_new']['fbs'].copy()
params=' '.join(game)
params_orig=params
if not params in team_list: params=abbrev(params,db['abbreviations'])
for a,b in teams.iteritems():
	if a != 'lastupdate':
		team1=b['team1'].lower().replace('(','').replace(')','')
		team2=b['team2'].lower().replace('(','').replace(')','')
		if params.count(' ') == 0: tclv=closest([params_orig,params.lower(),params.lower()+' StateZ',params.lower().replace('st','state')],[team1.lower(),team2.lower()])
		else: tclv=closest([params_orig,params.lower(),params.lower().replace('st','state')],[team1.lower(),team2.lower(),team1.lower()+team2.lower(),team2.lower()+team1.lower()])
		if tclv < closestval:
			closestval=tclv
			closests=a
bye=False
if closestval != 0 and params_orig in team_list:
	bye=True
	params=params_orig
	closest_bye_alt=''
	if closestval <= 3: closest_bye_alt=closests
	closests=''
elif closestval != 0 and params_orig.lower().replace(' ','') in conf_lower:
	closestval=100
	closests=''
#END MATCHING CODE


if dest=='footballbot' or dest=='footballtestbot': dest=origin



	#print calendar.timegm(datetime.datetime.utcnow().utctimetuple())-comment.created_utc
text_return=''
text_return_last=''
print closestval
print closests
if closests != '' and closestval <= 3:
	r_inst=praw.Reddit('Py')
	r_search=r_inst.search('[Game+Thread] '+teams[closests]['team1']+' '+teams[closests]['team2'],'cfb','comments',period='week')
	ourThread=False
	for thread in r_search:
		if not ourThread and thread.link_flair_text=='Game Thread': ourThread=thread
	if ourThread:
		#ourThread.replace_more_comments(limit=1,threshold=50)
		comments_scores={}
		comments_vals={}
		for comment in ourThread.comments:
			#print time.time()+8*3600-comment.created 
			try:
				if time.time()+8*3600-comment.created < secs:
					if comment.score >= 3:
						print 'yeahhh'
						comments_vals[comment.id]=comment
						comments_scores[comment.id]=float(float(comment.score)/float((time.time()+8*3600-comment.created)))
			except:
				pass
		#print comments_scores
		comments_scores = sorted(comments_scores.items(), key=operator.itemgetter(1))
		comments_scores.reverse()
		if comments_scores==None: comments_scores={}
		print comments_scores
		for comment in comments_scores:
			if comment != None:
				if text_return != '': text_return+=' | '
				if time.time()+8*3600-comments_vals[comment[0]].created > 60: tago=str(int((time.time()+8*3600-comments_vals[comment[0]].created)/60))+' mins'
				else: tago=str(int(time.time()+8*3600-comments_vals[comment[0]].created))+' secs'
				text_return+='\x02'+str(comments_vals[comment[0]].author)+' \x02('+str(comments_vals[comment[0]].score)+' points, '+tago+'): '+comments_vals[comment[0]].body
				text_return=text_return.replace('\r','').replace('\n','')
				if text_return_last != '' and len(text_return) > 410: text_return=text_return_last
			text_return_last=text_return
		text_return+=' *('+shorten_url(ourThread.url)+')*'
msg_type='PRIVMSG'
msg_dest=dest
if dest.lower().count('footballbot'): dest=origin
if text_return != '':
	db['msgqueue'].append([text_return,msg_dest,msg_type])
else:
	db['msgqueue'].append(["I couldn't find anything worth sharing. ",msg_dest,msg_type])