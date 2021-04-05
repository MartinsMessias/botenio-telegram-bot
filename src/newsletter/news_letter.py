from imap_tools import A, MailBox
from src.extra import credentials


def newsletter():
    """Returns Filipe Deschamps NewsLetter"""

    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993

    messages = []
    with MailBox(SMTP_SERVER).login(credentials.FROM_EMAIL, credentials.FROM_PWD, 'INBOX') as mailbox:
        emails = mailbox.fetch(
            A(from_='newsletter@filipedeschamps.com.br'))
        msg = [msg for msg in emails][-1]
        date = msg.headers['date'][0]
        msg = msg.text.split('\r\n\r\n')

        for m in msg:
            if 'https://' not in m:
                messages.append(m)
    return messages