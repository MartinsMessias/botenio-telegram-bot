from src.extra import bot, telegram, credentials, requests


def wikipedia(update, context):
    """Wikipedia search"""

    bot.sendChatAction(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING)

    user_input = update.message.text
    user_input = " ".join(filter(lambda x: x[0] != '/', user_input.split()))

    url = f'https://pt.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={user_input}'

    try:
        response = requests.get(url)
        pages = response.json()['query']['pages']

        for page_num in pages:
            extract = response.json(
            )['query']['pages'][str(page_num)]['extract']
        return context.bot.send_message(
            chat_id=update.effective_chat.id, text=extract)

    except BaseException:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Não encontrei nada sobre isso. ❌')
