import logging
import requests
import credentials

from random import randint
from time import sleep
from imap_tools import MailBox, A
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def define_command(update, context):
    """Return the commad called by user"""
    command = update.message.text.split(' ')[0]

    if len(update.message.text.split(' ')) <= 1:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Sintaxe dos comandos: \n{command} argumento')

    command = update.message.text.split(' ')[0]

    if command == '/shodan':
        return shodan(update, context)
    elif command == '/desciclopedia':
        return desciclopedia(update, context)
    elif command == '/wikipedia':
        return wikipedia(update, context)
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Mande algo que eu entenda por favor!')


def start(update, context):
    """Send a message when the command /start is issued."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='O pai tá ON, qual é a boa?')


def help(update, context):
    """Send a message when the command /help is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
        Comandos
        ―――――――――――――――――――――――――――
        ➤ /start - Inicia o bot.
        ➤ /shodan - Shodan search
        ➤ /wikipedia - Wikipedia search
        ➤ /desciclopedia - Desciclopedia search
        ➤ /newsletter - Notícias do mundo tech
        ➤ /trends - Twitter Trendings
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
    🍀 Boa sorte.\n
    {sorted(sort)}""")


def newsletter(update, context):
    """Send updated Filipe Deschamps NewsLetter"""

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

            for m in msg:
                if 'https://' not in m:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text=f'📍\n{m}')
                    sleep(0.5)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'⏳ ATUALIZADO EM ({date})')
    except Exception:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Erro ao tentar trazer newsletter ❌')


def trends(update, context):
    """Get Twitter trending topics"""
    try:
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
            context.bot.send_message(chat_id=update.effective_chat.id, 
            text=f"Assunto: {trend['name']}\nTweets: {trend['volume']}\n{'_' * 30}")
    except Exception:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Erro ao tentar trazer Trending Topics do Twitter ❌')


def shodan(update, context):
    user_input = update.message.text
    user_input = " ".join(filter(lambda x: x[0] != '/', user_input.split()))
    update.message.reply_text(
        f'🔍 Procurando computadores conectados a internet pela descrição: {user_input} ...')

    url = f'https://api.shodan.io/shodan/host/search?key={credentials.SHODAN_API_KEY}&query={user_input}'

    try:
        result = requests.get(url).json()
        results_count = 0

        if result['total'] > 0:
            for service in result['matches']:

                if not 'product' in service:
                    tipo = service['_shodan']['module']
                else:
                    tipo =  service['product']

                try:
                    msg = f"Tipo: {tipo}\nISP: {service['isp']}\nIP e PORTA: {service['ip_str']}:{service['port']}\nLOCALIZAÇÃO: {service['location']['city']} / {service['location']['country_name']}"
                    
                    context.bot.send_message(
                    chat_id=update.effective_chat.id, text=msg)
                    
                    results_count += 1

                    if results_count == 10:
                        break
                except:
                    results_count -= 1
                    #For non existent keys
                    continue
            
        return context.bot.send_message(chat_id=update.effective_chat.id, text=f" 🔍 Busca finalizada - Exibindo {results_count} de {result['total']} encontrados. 🔚")
    except Exception:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Erro ao tentar trazer dados do Shodan. Verifique a query de busca. ❌')


def desciclopedia(update, context):
    """Desciclopedia search"""

    user_input = update.message.text
    user_input = " ".join(filter(lambda x: x[0] != '/', user_input.split()))

    url = f'http://desciclopedia.org/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={user_input}'

    try:
        response = requests.get(url)
        pages = response.json()['query']['pages']

        for page_num in pages:
            extract = response.json(
            )['query']['pages'][str(page_num)]['extract']
        return context.bot.send_message(chat_id=update.effective_chat.id, text=extract)

    except Exception:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Não encontrei nada sobre isso. ❌')


def wikipedia(update, context):
    """Wikipedia search"""

    user_input = update.message.text
    user_input = " ".join(filter(lambda x: x[0] != '/', user_input.split()))

    url = f'https://pt.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={user_input}'

    try:
        response = requests.get(url)
        pages = response.json()['query']['pages']

        for page_num in pages:
            extract = response.json(
            )['query']['pages'][str(page_num)]['extract']
        return context.bot.send_message(chat_id=update.effective_chat.id, text=extract)

    except Exception:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Não encontrei nada sobre isso. ❌')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    context.bot.send_message(
        chat_id=credentials.ADMIN_CHAT_ID, text=f'Update {update} caused error {context.error}')


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

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, define_command))

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
