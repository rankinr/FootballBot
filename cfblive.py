time.sleep(1)
showStatus=False #show bot status?
overall_start_time=time.time()
#load live modules (this is quite intensive to load all these files every second - in the future, should cache and only reload on command)
os.system('ls -lah /home/fbbot/cfb/live_modules/ > .live_modules_dir')
live_modules=open('.live_modules_dir').read().split('\n')
os.system('rm .live_modules_dir')
modules=[]

for module in live_modules:
	if module.count('.py') != 0:
		module=module[::-1][module[::-1].find('.py'[::-1])+3:]
		module=module[:module.find(" ")][::-1]+'.py'
		modules.append(module)
loading_times={}
#exec(open('/home/fbbot/cfb/common_functions.py')) #load custom functions
for module in modules:
	#print module
	try:
		start_time=time.time()
		exec(open('/home/fbbot/cfb/live_modules/'+module).read())
		end_time=time.time()
		loading_times[module]=end_time-start_time
	except:
		errrl=traceback.format_exc()
		if str(errrl) != lasterrl: 
			errd=str(errrl)
			errd=errd[errd.find(':')+1:].strip().replace('\r',' ').replace('\n',' ')
			s.send('PRIVMSG #cfbtest :harkatmuld, there is an error in module '+module+': '+errd+'\r\n')
		lasterrl=str(errrl)
loading_times=sorted(loading_times.items(), key=operator.itemgetter(1))
loading_times.reverse()
if showStatus:
	os.system('clear')
	print "\r\n\r\n\r\nModule loading times:\r\n--\r\n\r\n"
total_module_load_time=0


# Send mass message to all users. First you must enable the variable on the first line, save. Then disable, and enable the other lines. Then, disable all after messages are sent.
#sentMass=False
if not sentMass:
	c=1
	for user in users_in_channel:
		s.send('PRIVMSG '+user+' Hello, '+user+'! Welcome back for another week of College Football. I have a new beta feature that will let you customize my interactions with you, including play-by-play updates. To try it, just send me the command !me in any channel or a private message. Please be aware that this feature is new. There may be errors-if you notice any, or have any feedback, please let harkatmuld know, either on IRC or on reddit. Thanks!\r\n')
		print "messaged "+user+' ('+str(c)+'/'+str(len(users_in_channel))+')'
		c+=1
	sentMass=True

for a in loading_times:
	if showStatus: print a[0]+': '+str(a[1])
	total_module_load_time+=a[1]
sent_ident=False
if not sent_ident:
	#s.send("PRIVMSG nickserv :identify %s\r\n"% 'w0^a%G5PjDQNpsW85cx9')
	sent_ident=True
overall_end_time=time.time()
if showStatus:
	print '\r\n\r\n'
	print 'Time for other processing and loading modules: '+str(overall_end_time-overall_start_time-total_module_load_time)
	print 'Total time per loop: '+str(overall_end_time-overall_start_time)
	print 'Users in channel: '
	print users_in_channel
#loop_time=time.time()-this_loop_start_time

if overall_end_time-overall_start_time > 1: s.send('PRIVMSG #cfbtest :harkatmuld, I had a long loop time. In total, the commands took '+str(overall_end_time-overall_start_time)+' seconds to execute.\r\n')