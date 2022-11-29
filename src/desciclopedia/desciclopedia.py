"""
Search for a term in the 'desciclopedia' wiki and return the first paragraph.
"""
import os
import requests
import telegram
from src.bot_instance import get_bot_instance


def desciclopedia(update, context):
    """Desciclopedia search"""
    bot = get_bot_instance()
    bot.sendChatAction(chat_id=update.effective_chat.id,
                       action=telegram.ChatAction.TYPING)
    if update.message is None:
        user_input = update.edited_message.text
    else:
        user_input = update.message.text
    user_input = " ".join(filter(lambda x: x[0] != '/', user_input.split()))

    url = 'http://desciclopedia.org/api.php?format=json&action=' \
        'query&prop=extracts&exintro&explaintext&redirects=1&titles=' + user_input

    try:
        response = requests.get(url, timeout=5)
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
