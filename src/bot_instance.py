import telegram
import os

def get_bot_instance():
    bot = None
    bot = telegram.Bot(token=os.environ.get('TELEGRAM_TOKEN'))
    return bot

if __name__ == '__main__':
    pass
