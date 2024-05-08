from datetime import datetime, timedelta
import json
from pushdeer import PushDeer
import os

PUSHKEY     = os.environ.get('PUSHKEY')
TITLE_HAX   = os.environ.get('TITLE_HAX')
TITLE_VC    = os.environ.get('TITLE_VC')
CONTENT     = os.environ.get('CONTENT')
HAX_DAY     = int(os.environ.get('HAX_DAY'))
VC_DAY      = int(os.environ.get('VC_DAY'))

def _notyfy(key, title, msg):
    pushdeer = PushDeer(pushkey=key)
    ok = pushdeer.send_markdown(title=title, desp=msg)
    if ok:
        print(f'Successfully sent notification.')
    else:
        print(f'Failed to send notification.')

def notify_hax(key, title, msgs):
    expire_time = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    title = title.format(expire_time)
    _notyfy(key, title, msgs)

def notify_vc(key, title, msgs):
    expire_time = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    title = title.format(expire_time)
    _notyfy(key, title, msgs)



try:
    with open('./.lastrun', 'r') as f:
        dates = json.load(f)
        last_run_date_hax = datetime.strptime(dates['hax'], '%Y-%m-%d')
        last_run_date_vc = datetime.strptime(dates['vc'], '%Y-%m-%d')
except FileNotFoundError:
    # 如果 .lastrun 文件不存在，假设上次运行是相应的天数前
    last_run_date_hax = datetime.now() - timedelta(days=HAX_DAY)
    last_run_date_vc = datetime.now() - timedelta(days=VC_DAY)
    with open('.lastrun', 'w') as f:
        dates = {
            'hax': last_run_date_hax.strftime('%Y-%m-%d'),
            'vc': last_run_date_vc.strftime('%Y-%m-%d')
        }
        json.dump(dates, f)

diff_hax = datetime.now() - last_run_date_hax
diff_vc = datetime.now() - last_run_date_vc

if diff_hax.days >= HAX_DAY:
    notify_hax(PUSHKEY, TITLE_HAX, CONTENT)
    dates['hax'] = datetime.now().strftime('%Y-%m-%d')

if diff_vc.days >= VC_DAY:
    notify_vc(PUSHKEY, TITLE_VC, CONTENT)
    dates['vc'] = datetime.now().strftime('%Y-%m-%d')

with open('.lastrun', 'w') as f:
    json.dump(dates, f)
