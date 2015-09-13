time.sleep(1)
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
for module in modules:
	start_time=time.time()
	exec(open('/home/fbbot/cfb/live_modules/'+module).read())
	end_time=time.time()
	loading_times[module]=end_time-start_time

loading_times=sorted(loading_times.items(), key=operator.itemgetter(1))
loading_times.reverse()
os.system('clear')
print "\r\n\r\n\r\nModule loading times:\r\n--\r\n\r\n"
total_module_load_time=0
for a in loading_times:
	print a[0]+': '+str(a[1])
	total_module_load_time+=a[1]

overall_end_time=time.time()
print '\r\n\r\n'
print 'Time for other processing and loading modules: '+str(overall_end_time-overall_start_time-total_module_load_time)
print 'Total time per loop: '+str(overall_end_time-overall_start_time)
print 'Users in channel: '
print users_in_channel

#loop_time=time.time()-this_loop_start_time
