from classes import Card
import datetime
from variables import bot, profile_messages
from variables import active_index
from variables import profiles
from telebot import types
from time import sleep


def check_int(ids: list):
    for i in ids:
        flag = i.isdigit()
        if not flag:
            return False
    return True


def get_string_card(card: Card):
    card_str = ""
    if 1 < card.value < 11:
        card_str += str(card.value)
    elif card.value == 1:
        card_str += "A"
    elif card.value == 11:
        card_str += "J"
    elif card.value == 12:
        card_str += "Q"
    elif card.value == 13:
        card_str += "K"
    if card.suit == 1:
        card_str += "♥ "
    elif card.suit == 2:
        card_str += "♦ "
    elif card.suit == 3:
        card_str += "♠ "
    elif card.suit == 4:
        card_str += "♣ "
    return card_str


def save_user_message(message):
    with open(
            'users/' + str(message.from_user.id) + '.txt',
            'a',
            encoding='utf-8'
    ) as f:
        f.write(str(datetime.datetime.now()) + " | " +
                str(message.from_user.id) + ": " +
                message.text + "\n")


def save_user_call(call):
    with open(
            'users/' + str(call.message.chat.id) + '.txt',
            'a',
            encoding='utf-8'
    ) as f:
        f.write(str(datetime.datetime.now()) + " | " +
                str(call.message.chat.id) + ": " +
                call.data + "\n")


def save_id_user(message):
    save_user_message(message)
    with open("users/ids.data",
              'r+',
              encoding='utf-8'
              ) as f:
        if str(message.from_user.id) not in f.read():
            something = f.read()
            f.write(something +
                    str(message.from_user.id) + " | " +
                    str(message.from_user.username) + " | " +
                    str(message.from_user.first_name) + " | " +
                    str(message.from_user.last_name) + "\n")


def get_bonus(call):
    index_profile = [n for n, x in enumerate(profiles) if x[:1] == [call.message.chat.id]].pop(0)
    index_message = [n for n, x in enumerate(profile_messages) if x[:1] == [call.message.chat.id]].pop(0)
    user = profiles[index_profile][1]
    if user.bonus_date == str(datetime.datetime.today()).split()[0]:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=profile_messages[index_message][1].message_id,
            text="Бонус уже использован, заходите завтра\n" + user.get_string(),
            reply_markup=do_profile_menu_markup()
        )
    else:
        user.bonus_date = str(datetime.datetime.today()).split()[0]
        user.money += 10000
        user.save_profile()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=profile_messages[index_message][1].message_id,
            text="На баланс было начислено 10000 у.е.\n" + user.get_string(),
            reply_markup=do_profile_menu_markup()
        )


def get_ids_usernames():
    with open("users/ids.data", 'r', encoding='utf-8') as f:
        something = f.read()
        return something


def get_ids():
    ids = []
    with open("users/ids.data", 'r', encoding='utf-8') as f:
        while True:
            chunk = f.readline()
            if chunk == '':
                break
            ids.append(chunk.split()[0])
    return ids


def do_ask_help_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Правила покера")
    btn2 = types.KeyboardButton("Правила Blackjack")
    btn3 = types.KeyboardButton("Что умеет бот?")
    btn4 = types.KeyboardButton("В главное меню")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup


def do_leave_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("В главное меню")
    markup.add(btn1)
    return markup


# функция для создания разметки клавиатуры для главного меню
def do_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Покер")
    btn2 = types.KeyboardButton("Blackjack")
    btn3 = types.KeyboardButton("Профиль")
    btn4 = types.KeyboardButton("/help")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup


# функция для создания разметки клавиатуры сообщения для игры в Blackjack
def do_blackjack_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Взять карту", callback_data='take_card')
    btn2 = types.InlineKeyboardButton(text="Удержать", callback_data='hold')
    markup.add(btn1, btn2)
    return markup


# функция для создания разметки клавиатуры сообщения для игры в покер
def do_poker_menu_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Создать игру", callback_data='create_poker_game')
    btn2 = types.InlineKeyboardButton(text="Игры", callback_data='show_poker_games')
    btn3 = types.InlineKeyboardButton(text="Закрыть меню", callback_data='return_to_menu')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


def do_profile_menu_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Взять бонус", callback_data='profile_bonus')
    btn2 = types.InlineKeyboardButton(text="Закрыть меню", callback_data='exit_profile')
    btn3 = types.InlineKeyboardButton(text="Сменить имя", callback_data='change_name')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


def do_blackjack_bet_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Поднять ставку x2", callback_data='blackjack_up')
    btn2 = types.InlineKeyboardButton(text="Понизить ставку x2", callback_data='blackjack_down')
    btn3 = types.InlineKeyboardButton(text="Максимальная ставка", callback_data='blackjack_max')
    btn4 = types.InlineKeyboardButton(text="Минимальная ставка", callback_data='blackjack_min')
    btn5 = types.InlineKeyboardButton(text="Своя ставка", callback_data='blackjack_set')
    btn6 = types.InlineKeyboardButton(text="Начать игру", callback_data='blackjack_start')
    btn7 = types.InlineKeyboardButton(text="Закрыть меню", callback_data='blackjack_stop')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    markup.add(btn6)
    markup.add(btn7)
    return markup


def do_poker_list_markup(index: int):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=str(active_index[index][1] + 1), callback_data='first_poker')
    btn2 = types.InlineKeyboardButton(text=str(active_index[index][1] + 2), callback_data='second_poker')
    btn3 = types.InlineKeyboardButton(text=str(active_index[index][1] + 3), callback_data='third_poker')
    btn4 = types.InlineKeyboardButton(text=str(active_index[index][1] + 4), callback_data='fourth_poker')
    btn5 = types.InlineKeyboardButton(text=str(active_index[index][1] + 5), callback_data='fifth_poker')
    btn6 = types.InlineKeyboardButton(text="Назад", callback_data='back_poker')
    btn7 = types.InlineKeyboardButton(text="Далее", callback_data='next_poker')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    markup.add(btn6, btn7)


def send_long_message(message, data_string: str):
    if len(data_string) > 4096:
        for i in range(0, len(data_string), 4096):
            bot.send_message(
                message.from_user.id,
                data_string[i:i + 4096]
            )
            sleep(0.5)
    else:
        bot.send_message(
            message.from_user.id,
            data_string
        )


def change_name(message):
    index_profile = [n for n, x in enumerate(profiles) if x[:1] == [message.from_user.id]].pop(0)
    index_message = [n for n, x in enumerate(profile_messages) if x[:1] == [message.from_user.id]].pop(0)
    user = profiles[index_profile][1]
    user.name = str(message.text)
    user.save_profile()
    bot.edit_message_text(
        chat_id=message.from_user.id,
        text=user.get_string(),
        reply_markup=do_profile_menu_markup(),
        message_id=profile_messages[index_message][1].message_id
    )


def send_profile_message(user_id: int):
    bot.send_message(
        user_id,
        "Загрузка вашего профиля...",
        reply_markup=types.ReplyKeyboardRemove()
    )
    profile = [n for n, x in enumerate(profiles) if x[:1] == [user_id]]
    profile_messages.append(
        [
            user_id,
            bot.send_message(
                user_id,
                profiles[profile.pop(0)][1].get_string(),
                reply_markup=do_profile_menu_markup()
            )
        ]
    )


def send_poker_message(user_id: int):
    bot.send_message(
        user_id,
        "Запуск покер меню...",
        reply_markup=types.ReplyKeyboardRemove()
    )
    sleep(1)
    active_index.append(
        [
            user_id,
            0,
            bot.send_message(
                user_id,
                "Это меню игры Покер\nВыберите действие:",
                reply_markup=do_poker_menu_markup()
            )
        ]
    )
