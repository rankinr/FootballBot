import urllib,urlparse,time,random,re,traceback
import os,json
from bs4 import BeautifulSoup
from mechanize import Browser
startingat=time.time()
from collections import OrderedDict
from HTMLParser import HTMLParser

lloop=time.time()
llen=0
yamsg=[]
db={}
exec(open('/home/fbbot/cfb/sload.py').read())
teamsold=json.loads(sql.unique_get('data','games'))
db['colors']=json.loads(sql.unique_get('data','colors'))
color_list=db['colors']

exec(open('/home/fbbot/cfb/common_functions.py').read())

overallc=0
while overallc < 10000 and time.time() < startingat+60*4.8:
	exec open('/home/fbbot/cfb/updaters/parselive.py').read()
