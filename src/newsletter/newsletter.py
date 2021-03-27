from imap_tools import MailBox, A
from time import sleep
from src.extra import bot, telegram, credentials


def newsletter(update, context):
    """Send updated Filipe Deschamps NewsLetter"""
    bot.sendChatAction(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING)

    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993

    messages = []
    try:
        with MailBox(SMTP_SERVER).login(credentials.FROM_EMAIL, credentials.FROM_PWD, 'INBOX') as mailbox:
            emails = mailbox.fetch(
                A(from_='newsletter@filipedeschamps.com.br'))
            msg = [msg for msg in emails][-1]
            date = msg.headers['date'][0]
            msg = msg.text.split('\r\n\r\n')

            bot.sendChatAction(
                chat_id=update.effective_chat.id,
                action=telegram.ChatAction.TYPING)

            for m in msg:
                if 'https://' not in m:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text=f'📍\n{m}')
                    sleep(0.45)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'⏳ ATUALIZADO EM ({date})')
    except BaseException:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Erro ao tentar trazer newsletter ❌')
