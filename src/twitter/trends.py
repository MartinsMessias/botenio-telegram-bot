from src.extra import bot, telegram, credentials, requests
from time import sleep


def trends(update, context):
    """Get Twitter trending topics"""

    bot.sendChatAction(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING)

    try:
        hed = {'Authorization': 'Bearer ' + credentials.TWITTER_TOKEN}

        url = 'https://api.twitter.com/1.1/trends/place.json?id=1'
        response = requests.get(url, headers=hed)

        data = []

        for trend in response.json()[0]['trends']:

            clean_trend = {}

            if trend['promoted_content'] is None:
                clean_trend['name'] = trend['name']
                clean_trend['volume'] = trend['tweet_volume']
                clean_trend['url'] = trend['url']

            data.append(clean_trend)

        for trend in data:
            sleep(0.5)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Assunto: {trend['name']}\nTweets: {trend['volume']}\n{'_' * 30}")
    except BaseException:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Erro ao tentar trazer Trending Topics do Twitter ❌')
