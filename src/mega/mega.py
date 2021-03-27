import random


def mega(update, context):
    """Send 6 random numbers"""
    sort = []

    while len(sort) < 6:
        number = random.randint(1, 60)

        if sort.count(number) == 0:
            sort.append(number)
    return context.bot.send_message(chat_id=update.effective_chat.id, text=f"""
    🍀 Boa sorte.\n
    {sorted(sort)}""")
