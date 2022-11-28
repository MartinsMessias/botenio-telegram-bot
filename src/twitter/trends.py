from src.extra import bot, telegram, credentials, requests
from time import sleep


def trends(update, context):
    """Get Twitter trending topics"""

    bot.sendChatAction(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING)

    try:
        hed = {'Authorization': 'Bearer ' + credentials.TWITTER_TOKEN}

        url = 'https://api.twitter.com/1.1/trends/place.json?id=455827'
        response = requests.get(url, headers=hed)

        data = []

        for trend in response.json()[0]['trends']:

            clean_trend = {}

            if trend['promoted_content'] is None:
                volume = trend['tweet_volume']
                if not volume or volume == "":
                    continue
                clean_trend['name'] = trend['name']
                clean_trend['volume'] = int(volume)
                clean_trend['url'] = trend['url']

            data.append(clean_trend)

        data = sorted(data, key=lambda d: d['volume'], reverse=True)

        message = "🐥 Top 10 tendências no Brasil\n"
        for trend in data[:10]:
            message += f'\n {data.index(trend) + 1} - {trend["name"]} \nMensões: {trend["volume"]}\n'

        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message)
    except BaseException:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❌ Erro ao tentar trazer Trending Topics do Twitter ❌')
