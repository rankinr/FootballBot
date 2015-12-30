import json, os
exec(open('/home/fbbot/cfb/sload.py').read())
exec(open('/home/fbbot/cfb/common_functions.py').read())
bets=json.loads(sql.unique_get('data','bets'))
games=json.loads(sql.unique_get('data','games_new'))
games['fbs']['AuburnMemphis']['status']='notfi'
bets['harkatmuld']['AuburnMemphis']=['Memphis','-99',30]
sql.unique_set('data','bets',json.dumps(bets))
sql.unique_set('data','games_new',json.dumps(games))
os.system('python /home/fbbot/cfb/updaters/new_parser.py')