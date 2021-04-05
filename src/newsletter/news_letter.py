import json
import os
from dataclasses import replace
from datetime import date

import redis
from imap_tools import A, MailBox

from src.extra import credentials

# Heroku Redis to Go
cache = redis.from_url(os.environ.get("REDISTOGO_URL"))


def newsletter():
    """Returns Filipe Deschamps NewsLetter"""
    today = str(date.today())

    if cache.exists(today):
        newsletters = cache.get(today).decode('utf-8')
        return json.loads(newsletters)

    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993

    messages = []
    with MailBox(SMTP_SERVER).login(credentials.FROM_EMAIL, credentials.FROM_PWD, 'INBOX') as mailbox:
        emails = mailbox.fetch(
            A(from_='newsletter@filipedeschamps.com.br'))
        msg = [msg for msg in emails][-1]
        data = msg.headers['date'][0]
        msg = msg.text.split('\r\n\r\n')
        msg = msg.replace('\r\n', ' ')

        for m in msg:
            if 'https://' not in m:
                messages.append(m)

    messages.append(data)
    cache.mset({today: json.dumps(messages)})
    return messages