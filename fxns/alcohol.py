"""
Returns my current blood alcohol level
"""
if dest.lower() == 'footballbot': dest = origin
db['msgqueue'].append(['My current circuit alcohol level is ' + str(round(
    dlevel / 100, 2)) + '%.', dest])
