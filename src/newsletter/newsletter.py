from imap_tools import MailBox, A
from time import sleep
from src.extra import bot, telegram, credentials
from src.newsletter import news_letter
from datetime import date


def newsletter(update, context):
    """Send updated Filipe Deschamps NewsLetter"""

    try:
        bot.sendChatAction(chat_id=update.effective_chat.id,
                           action=telegram.ChatAction.TYPING)

        msg = news_letter.newsletter()

        for m in msg:
            bot.sendChatAction(chat_id=update.effective_chat.id,
                               action=telegram.ChatAction.TYPING)
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f'📍\n{m}')

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'CACHE ATUALIZADO EM ({str(date.today())})')
    except BaseException:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Erro ao tentar trazer newsletter ❌')
