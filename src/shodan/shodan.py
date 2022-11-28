import random
from src.extra import bot, telegram, credentials, requests


def shodan(update, context):
    bot.sendChatAction(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING)

    if update.message is None:
        user_input = update.edited_message.text
    else:
        user_input = update.message.text
    user_input = " ".join(filter(lambda x: x[0] != '/', user_input.split()))

    results_count_limit = 10

    if '|' in user_input:
        user_input = user_input.split('|')
        results_count_limit = int(user_input[1].replace(' ', ''))
        user_input = user_input[0]

    update.message.reply_text(
        f'🔍 Procurando computadores conectados a internet pela descrição: {user_input}...')

    url = f'https://api.shodan.io/shodan/host/search?key={credentials.SHODAN_API_KEY}&query={user_input}'

    bot.sendChatAction(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING)

    try:
        result = requests.get(url).json()
        results_count = 0

        if result['total'] == 0 or not result:
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Sem resultados')

        random.shuffle(result['matches'])
        for service in result['matches']:

            if results_count == results_count_limit:
                break

            try:
                msg = f"Tipo: {service['product']}\nISP: {service['isp']}\nIP e PORTA: {service['ip_str']}:{service['port']}\nLOCALIZAÇÃO: {service['location']['city']} / {service['location']['country_name']}"

                response = context.bot.send_message(
                    chat_id=update.effective_chat.id, text=msg)

                if response['message_id']:
                    results_count += 1
                else:
                    results_count -= 1
            except BaseException:
                pass

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f" 🔍 Busca finalizada - Exibindo melhores {results_count} de {result['total']} encontrados.")
    except BaseException:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Erro ao tentar trazer dados do Shodan.\nVerifique a query de busca e tente novamente. ❌')
