import json, fcntl, time, socket, string, random, time, os, hashlib, urllib, sys, traceback, HTMLParser
fdb = open('db.json', 'r')
fcntl.flock(fdb, fcntl.LOCK_EX)
db = json.load(fdb)
fcntl.flock(fdb, fcntl.LOCK_UN)
for z, u in db['scorerequests'].iteritems():
    sr = []
    for a in u:
        sr.append(a[0])
        sr.append(a[1])
    ad = []
    for a in sr:
        if sr.count(a) > 10 and ad.count(a) == 0:
            print z + ': ' + a
            ad.append(a)
