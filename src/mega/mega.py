import telegram
import random
import prettytable as pt
from telegram import ParseMode
from src.mega.frequencia import check_frequence, get_info, check_frequence_range
from src.bot_instance import get_bot_instance


def mega(update, context):
    """Send 6 random numbers"""
    bot = get_bot_instance()
    bot.sendChatAction(
    chat_id=update.effective_chat.id,
    action=telegram.ChatAction.CHOOSE_STICKER)
    try:
        
        sort = []

        while len(sort) < 6:
            number = random.randint(1, 60)

            if sort.count(number) == 0:
                sort.append(number)

        sorted_numbers = sorted(sort)
        freq_sum = 0

        table = pt.PrettyTable(['Número', 'Sorteios'])
        table.align['Numero'] = 'l'
        table.align['Sorteios'] = 'r'

        for num in sorted_numbers:
            freq, _ = check_frequence(num)
            table.add_row([num, freq])
            freq_sum += freq
        
        table = f'<pre>{table}</pre>'
        message = f'''<b>🍀 Gerador de números - Mega-Sena</b>


        {sorted_numbers[0]} - {sorted_numbers[1]} - {sorted_numbers[2]} - {sorted_numbers[3]} - {sorted_numbers[4]} - {sorted_numbers[5]}

Quantas vezes cada número já foi sorteado:

{table}
🔥 {freq_sum}

    {get_info()}

    Boa sorte!'''
        return context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(e)
        return context.bot.send_message(chat_id=update.effective_chat.id, text='Aou! Sem spammar. Tá achando que eu tô hospedado no na Nasa?')