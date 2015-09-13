try:
	readbuffer=readbuffer+s.recv(1024)
	temp=string.split(readbuffer, "\n")
	readbuffer=temp.pop( )
	for line in temp:
		line=string.rstrip(line)
		#print line
		line=string.split(line)
		lines.append(line)
		#print line
except: nodata=1