team=' '.join(params).strip()
print db['logos']
print team
logos=artolower(db['logos'].copy())
if team in logos:
	print '2'
	colors={'white':'0','black':'1','blue':'2','green':'3','red':'4','maroon':'5','purple':'6','orange':'7','yellow':'8','light green':'9','teal':'10','cyan':'11','light blue':'12','pink':'13','grey':'14','silver':'15'}
	lines=logos[team].split('\r\n')
	tosend=''
	for line in lines:
		while line.count('(') != 0:
			paren=line[line.find('(')+1:line.find(')')]
			col1=colors[paren[:paren.find(',')].strip().lower()]
			col2=colors[paren[paren.find(',')+1:].strip().lower()]
			line=line[:line.find('(')]+chr(3)+col1+','+col2+line[line.find(')')+1:]
		tosend+='PRIVMSG harkatmuld :'+line+'\r\n'
		print line
	s.send(tosend)
#(black, black).....(white, white).....(black, black)......
# (black, black).(green, green)...(black, black).(white, white)...(black, black).(green, green)....(black, black).
# (black,black).(green,green)..(black,black).(green,green)..(black,black).(green,green)...(black,black).(green,green)..(black,black).
# (black,black).(green,green)...(black,black).(green,green)...(black,black).(green,green)....(black,black).
#(black,black).(green,green).......(black,black).(green,green).......(black,black).

