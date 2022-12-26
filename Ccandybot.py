import telebot
from random import randint
from random import choice

bot = telebot.TeleBot("5981765117:AAGB-Kghd-4qFWyx2QGl23cap9_j0dqFScg")

CCandy = dict()
enable_game = dict()
turn = dict()
name = choice(['Грильяж', 'Пралине', 'Марципан'])


def handle_game_proc(message):
    global enable_game
    try:
        if enable_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            bot.send_message(message.chat.id,'Не-а, от 1 до 28, не меньше, не больше.')
            return False
    except KeyError:
        enable_game[message.chat.id] = False
        bot.send_message(message.chat.id,'Это даже не число)')
        if enable_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global turn, CCandy, enable_game, name
    bot.reply_to(message, "Начнем!")
    CCandy[message.chat.id] = 117
    turn[message.chat.id] = choice([name, message.from_user.first_name])
    bot.send_message(message.chat.id, f'Твоим соперником будет {name}')
    bot.send_message(message.chat.id, f'Начинает {turn[message.chat.id]}')
    enable_game[message.chat.id] = True
    if turn[message.chat.id] == name:
        take = randint(1, CCandy[message.chat.id] % 29)
        CCandy[message.chat.id] -= take
        bot.send_message(message.chat.id, f'{name} взял {take}')
        bot.send_message(message.chat.id, f'Осталось {CCandy[message.chat.id]}')
        turn[message.chat.id] = message.from_user.first_name


@bot.message_handler(func=handle_game_proc)
def game_process(message):
    global CCandy, turn, enable_game, name
    if turn[message.chat.id] == message.from_user.first_name:
        if CCandy[message.chat.id] > 28:
            CCandy[message.chat.id] -= int(message.text)
            bot.send_message(message.chat.id, f'Осталось {CCandy[message.chat.id]}')
            if CCandy[message.chat.id] >= 28:
                take = randint(1, 29)
                CCandy[message.chat.id] -= take
                bot.send_message(message.chat.id, f'{name} взял {take}')
                bot.send_message(message.chat.id, f'Осталось {CCandy[message.chat.id]}')
                if CCandy[message.chat.id] <= 28:
                    bot.send_message(message.chat.id, f'{message.from_user.first_name} победил!')
                    enable_game[message.chat.id] = False
            else:
                bot.send_message(message.chat.id, f'{name} победил!')
                enable_game[message.chat.id] = False
        else:
            bot.send_message(message.chat.id, f'{name} победил!')
            enable_game[message.chat.id] = False


bot.infinity_polling()
