import json
exec(open('/home/fbbot/cfb/sload.py').read())
exec(open('/home/fbbot/cfb/common_functions.py').read())
cash=json.loads(sql.unique_get('data','cash'))
for a in cash:
	cash[a]=cash[a]+50
sql.unique_set('data','cash',json.dumps(cash))