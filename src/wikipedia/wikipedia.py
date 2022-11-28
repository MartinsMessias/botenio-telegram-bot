from src.extra import bot, telegram, credentials, requests


def wikipedia(update, context):
    """Wikipedia search"""

    bot.sendChatAction(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING)

    if update.message is None:
        user_input = update.edited_message.text
    else:
        user_input = update.message.text
    user_input = " ".join(filter(lambda x: x[0] != '/', user_input.split()))

    url = f'https://pt.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={user_input}'

    try:
        response = requests.get(url)
        pages = response.json()['query']['pages']

        for page_num in pages:
            extract = response.json(
            )['query']['pages'][str(page_num)]['extract']

        text = f'''
        🔎 Pesquisando sobre: {user_input}\n
        {extract}

        Fonte: Wikipédia
        '''
        return context.bot.send_message(
            chat_id=update.effective_chat.id, text=text)

    except BaseException:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Não encontrei nada sobre isso. ❌')
