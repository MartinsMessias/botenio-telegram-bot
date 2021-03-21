import logging
import requests
import credentials
import shodan

from random import randint
from time import sleep
from imap_tools import MailBox, A
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text='Eu tô ligado blz.')


def shodan(update, context):
    api = shodan.Shodan(SHODAN_API_KEY)
    result = api.search(update.message.text)

    # Loop through the matches and print each IP
    for service in result['matches']:
        context.bot.send_message(chat_id=update.effective_chat.id, text=service['ip_str'])

def echo(update, context):
    """Send wiki"""
    url = f'http://desciclopedia.org/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={update.message.text}'
    #url = f'https://pt.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={update.message.text}'
    sleep(1)
    response = requests.get(url)
    pages = response.json()['query']['pages']

    for page_num in pages:
        extract = response.json()['query']['pages'][str(page_num)]['extract']
    return context.bot.send_message(chat_id=update.effective_chat.id, text=extract)


def newsletter(update, context):
    """Send updated Filipe Deschamps NewsLetter"""

    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993

    messages = []
    with MailBox(SMTP_SERVER).login(credentials.FROM_EMAIL, credentials.FROM_PWD, 'INBOX') as mailbox:
        emails = mailbox.fetch(A(from_='newsletter@filipedeschamps.com.br'))
        msg = [msg for msg in emails][-1]
        date = msg.headers['date'][0]
        msg = msg.text.split('\r\n\r\n')
        for m in msg:
            sleep(0.5)
            if 'https://' not in m:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'📍\n{m}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'⏳ ATUALIZADO EM ({date})')


def help(update, context):
    """Send a message when the command /help is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
        Comandos
        ―――――――――――――――――――――――――――
        ➤ /start - Inicia o bot.
        ➤ /trends - Topic trends Twitter.
        ➤ /mega - Números para você jogar na mega.
        ➤ /help - Exibe a ajuda.

        Tem dicas de funções? Fale com pai. Ele tá ON.
        🗨️ @mrcodess
    ''')


def mega(update, context):
    """Send 6 random numbers"""
    sort = []
    while len(sort) < 6:
        number = randint(1, 60)
        if sort.count(number) == 0:
            sort.append(number)
    return context.bot.send_message(chat_id=update.effective_chat.id, text=f"""
    🍀 Boa sorte. 

    {sorted(sort)}

    Não esquece de me mandar um pouco.
    """)


def trends(update, context):
    """Get Twitter trending topics"""

    hed = {'Authorization': 'Bearer ' + credentials.TWITTER_TOKEN}

    url = 'https://api.twitter.com/1.1/trends/place.json?id=1'
    response = requests.get(url, headers=hed)

    data = []

    for trend in response.json()[0]['trends']:

        clean_trend = {}

        if trend['promoted_content'] == None:
            clean_trend['name'] = trend['name']
            clean_trend['volume'] = trend['tweet_volume']
            clean_trend['url'] = trend['url']

        data.append(clean_trend)

    for trend in data:
        sleep(0.5)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"""
            Assunto: {trend['name']}
            Tweets: {trend['volume']}
            Link: {trend['url']}
            {"_" * 30}
        """)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    context.bot.send_message(chat_id='1036725444', text=f'Update {update} caused error {context.error}')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(credentials.TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("trends", trends))
    dp.add_handler(CommandHandler("mega", mega))
    dp.add_handler(CommandHandler("newsletter", newsletter))
    dp.add_handler(CommandHandler("shodan", shodan))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
