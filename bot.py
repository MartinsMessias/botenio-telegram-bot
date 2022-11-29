"""
Main script
"""
import logging
import os
import telegram

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Import all functions here
from src.desciclopedia.desciclopedia import desciclopedia
from src.mega.mega import mega
from src.shodan.shodan import shodan
from src.twitter.trends import trends
from src.wikipedia.wikipedia import wikipedia


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
bot = telegram.Bot(token=os.environ.get('TELEGRAM_TOKEN'))


def define_command(update, context):
    """Return the commad called by user"""
    valid_cmd = ['/shodan', '/desciclopedia', '/wikipedia']
    if update.message is not None:
        command = update.message.text
    else:
        command = update.edited_message.text

    command_splited = command.split(' ')[0]

    if len(command.split(' ')) <= 1 and command_splited in valid_cmd:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Sintaxe dos comandos: \n{command_splited} argumento')

    if command_splited == '/shodan':
        return shodan(update, context)
    elif command_splited == '/desciclopedia':
        return desciclopedia(update, context)
    elif command_splited == '/wikipedia':
        return wikipedia(update, context)
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Mande algo que eu entenda por favor!')


def start(update, context):
    """Send a message when the command /start is issued."""
    bot.sendChatAction(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='O pai tá ON, qual é a boa? ')


def other_help(update, context):
    """Send a message when the command /help is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
        Comandos
        ―――――――――――――――――――――――――――
        ➤ /start - Inicia o bot.
        ➤ /shodan - Shodan search
        ➤ /wikipedia - Wikipedia search
        ➤ /desciclopedia - Desciclopedia search
        ➤ /trends - Twitter Trendings
        ➤ /mega - Números para você jogar na mega.

        ➤ /help - Exibe a ajuda.

        Tem dicas de funções? Fale com pai. Ele tá ON.
        🗨️ @mrcodess
    ''')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    context.bot.send_message(
        chat_id=os.environ.get('ADMIN_CHAT_ID'),
        text=f'Update {update} caused error {context.error}')


def main():
    """Start the bot."""
    updater = Updater(os.environ.get('TELEGRAM_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", other_help))
    dp.add_handler(CommandHandler("trends", trends))
    dp.add_handler(CommandHandler("mega", mega))
    # dp.add_handler(CommandHandler("newsletter", newsletter))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, define_command))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
