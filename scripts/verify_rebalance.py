import re
from datetime import datetime

LOG = 'logs/rebalancer.log'
MARK = datetime.utcnow().strftime('%Y-%m-%dT%H:%M')

with open(LOG) as f:
    tail = f.readlines()[-100:]

buys, sells = [], []
for line in tail:
    if 'safe_execute' in line:
        if 'BUY' in line:
            buys.append(line.strip())
        if 'SELL' in line:
            sells.append(line.strip())

print('→ BUY orders:')
print('\n'.join(buys))
print('\n→ SELL orders:')
print('\n'.join(sells))
