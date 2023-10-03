from pushdeer import PushDeer
from datetime import datetime, timedelta
import argparse
import os

PUSHKEY = os.environ.get('PUSHKEY')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str, default=None)
    parser.add_argument('--content', type=str, default=None)
    parser.add_argument('--days', type=int, default=None)
    args = parser.parse_args()

    title = args.title
    msgs = args.content
    day = args.days

    expire_time = (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
    title = title.format(expire_time)

    pushdeer = PushDeer(pushkey=PUSHKEY)
    pushdeer.send_markdown(title=title, desp=msgs)
