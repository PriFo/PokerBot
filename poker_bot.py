import telebot.types
import os
import blackjack
import poker
from variables import bot, profile_messages, poker_games, active_index, offline_blackjack_games, profiles
from classes import Profile
from poker import poker_game_index
import bot_logic
import config


# функция для обработки сообщения /start
@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    bot_logic.save_id_user(message)
    bot.send_message(
        message.from_user.id,
        "Здравствуй, я бот, который может проводить онлайн покер игры с несколькими игроками. Если тебе "
        "интересно, начать пользоваться мной, то выбери любой из пунктов меню.\n\nЕсли ты хочешь уточнить "
        "правила, то введи команду /help",
        reply_markup=bot_logic.do_main_markup()
    )


@bot.message_handler(commands=['active_blackjack'])
def show_blackjack_index(message: telebot.types.Message):
    text_message = '[\n'
    for i in offline_blackjack_games:
        text_message += str(i[0]) + ',\n'
    text_message += ']'
    bot.send_message(
        message.from_user.id,
        text_message
    )


@bot.message_handler(commands=['profile_messages'])
def show_profile_messages_index(message: telebot.types.Message):
    text_message = '[\n'
    for i in profile_messages:
        text_message += str(i[0]) + ',\n'
    text_message += ']'
    bot.send_message(
        message.from_user.id,
        text_message
    )


# функция для демонстрации всех административных функций бота
@bot.message_handler(commands=['commands'])
def show_commands_message(message: telebot.types.Message):
    bot_logic.save_user_message(message)
    bot.send_message(
        message.from_user.id,
        config.all_commands
    )


@bot.message_handler(commands=['log'])
def log_message(message: telebot.types.Message):
    bot_logic.save_user_message(message)
    ids = message.text.split()[1:]
    log_list = []
    if bot_logic.check_int(ids):
        with open(
                'users/' + ids[0] + '.txt',
                'r',
                encoding='utf-8'
        ) as f:
            while True:
                chunk = f.readline()
                if not chunk == '':
                    log_list.append(chunk)
                else:
                    break
        log_string = ''
        log_len = len(log_list)
        if log_len <= 128:
            for i in log_list:
                log_string += i
        else:
            for i in log_list[log_len - 128:log_len]:
                log_string += i
        bot_logic.send_long_message(message, log_string)
        bot.send_message(
            message.from_user.id,
            "Записей в файле: " + str(log_len)
        )


@bot.message_handler(commands=['poker'])
def show_poker_games(message: telebot.types.Message):
    bot_logic.save_user_message(message)
    list_of_games = "[\n"
    for i in poker_games:
        list_of_games += "\t" + str(i[0]) + ",\n\t[\n"
        for j in i[1]:
            list_of_games += "\t\t" + str(j[0]) + ",\n\t\t[ "
            for k in j[1].cards:
                list_of_games += str(k.value) + " | " + str(k.suit) + ", "
            list_of_games += "],\n\t\t" + str(j[2]) + "\n],"
        list_of_games += "\t],\n"
        list_of_games += "\t" + str(i[2]) + ",\n"
        list_of_games += "\t" + str(i[3]) + ",\n"
        list_of_games += "\t" + str(i[4]) + "],\n"
    list_of_games += "]"
    bot_logic.send_long_message(message, list_of_games)


# функция для демонстрации пользовательских id и их username
@bot.message_handler(commands=['show_ids'])
def show_ids_message(message: telebot.types.Message):
    bot_logic.save_user_message(message)
    bot_logic.send_long_message(message, bot_logic.get_ids_usernames())


@bot.message_handler(commands=['message'])
def send_message(message: telebot.types.Message):
    bot_logic.save_user_message(message)
    index = message.text.find(":")
    text = message.text[0:index - 1].split()[1:]
    if bot_logic.check_int(text) or text[0] == "all":
        user_message = str(message.text[index + 2:])
        user_message += "\nСообщение было отправлено от "
        if message.from_user.username is not None:
            user_message += "@" + str(message.from_user.username)
        else:
            user_message += str(message.from_user.first_name)
        if not text[0] == "all":
            for i in text:
                bot.send_message(
                    i,
                    user_message
                )
        else:
            for i in bot_logic.get_ids():
                bot.send_message(
                    i,
                    user_message
                )


# функция для демонстрации всех возможностей бота
@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    bot_logic.save_id_user(message)
    bot.send_message(
        message.from_user.id,
        config.ask_for_help,
        reply_markup=bot_logic.do_ask_help_markup()
    )


# функция для обработки клавиш клавиатуры сообщений
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery):
    bot_logic.save_user_call(call)
    if call.data == 'take_card':
        blackjack.take_card(call)

    elif call.data == 'hold':
        blackjack.hold_cards(call)

    elif call.data == 'create_poker_game':

        bot.send_message(
            call.message.chat.id,
            'Небольшие технические шоколадки...',
            reply_markup=bot_logic.do_leave_markup()
        )

    elif call.data == 'show_poker_games':
        poker.send_poker_games(
            call,
            [n for n, x in enumerate(active_index) if x[:1] == [call.message.chat.id]].pop(0)
        )

    elif call.data == 'profile_bonus':
        bot_logic.get_bonus(call)

    elif call.data == 'change_name':
        index = [n for n, x in enumerate(profile_messages) if x[:1] == [call.message.chat.id]].pop(0)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=profile_messages[index][1].message_id,
            text="Введите имя, которые вы хотите использовать",
        )

        bot.register_next_step_handler(profile_messages[index][1], bot_logic.change_name)

    elif call.data == 'return_to_menu':
        index = [n for n, x in enumerate(active_index) if x[:1] == [call.message.chat.id]]
        if index:
            index = index.pop(0)
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=active_index[index][2].message_id,
                reply_markup=None
            )
            active_index.pop(index)
        bot.send_message(
            call.message.chat.id,
            config.main_menu,
            reply_markup=bot_logic.do_main_markup()
        )

    elif call.data == 'exit_profile':
        profile_message = [n for n, x in enumerate(profile_messages) if x[:1] == [call.message.chat.id]]
        if profile_message:
            index = profile_message.pop(0)
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=profile_messages[index][1].message_id,
                reply_markup=None
            )
            profile_messages.pop(index)
        bot.send_message(
            call.message.chat.id,
            config.main_menu,
            reply_markup=bot_logic.do_main_markup()
        )
        pass

    elif call.data == 'blackjack_up':
        blackjack.change_bet_blackjack(call, 1)
        pass

    elif call.data == 'blackjack_down':
        blackjack.change_bet_blackjack(call, 2)
        pass

    elif call.data == 'blackjack_max':
        blackjack.change_bet_blackjack(call, 3)
        pass

    elif call.data == 'blackjack_min':
        blackjack.change_bet_blackjack(call, 4)
        pass

    elif call.data == 'blackjack_set':
        blackjack.change_bet_blackjack(call, 5)
        pass

    elif call.data == 'blackjack_start':
        hand_user = blackjack.get_hand(call.message.chat.id)
        if hand_user:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=str(blackjack.show_hand_blackjack(call.message.chat.id)),
                reply_markup=bot_logic.do_blackjack_markup(),
                message_id=hand_user[4].message_id
            )
            hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [call.message.chat.id]]
            offline_blackjack_games.pop(hand.pop())
            offline_blackjack_games.append(hand_user)

    elif call.data == 'blackjack_stop':
        hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [call.message.chat.id]]
        if hand:
            if len(hand) > 1:
                for _ in hand:
                    index = [n for n, x in enumerate(offline_blackjack_games) if x[:1] ==
                             [call.message.chat.id]].pop(0)
                    bot.edit_message_reply_markup(
                        chat_id=call.message.chat.id,
                        message_id=offline_blackjack_games[index][4].message_id,
                        reply_markup=None
                    )
                    offline_blackjack_games.pop(index)
            else:
                hand = hand.pop(0)
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=offline_blackjack_games[hand][4].message_id,
                    reply_markup=None
                )
                offline_blackjack_games.pop(hand)
        bot.send_message(
            call.message.chat.id,
            config.main_menu,
            reply_markup=bot_logic.do_main_markup()
        )
        pass

    elif call.data == 'first_poker':
        pass

    elif call.data == 'second_poker':
        pass

    elif call.data == 'third_poker':
        pass

    elif call.data == 'fourth_poker':
        pass

    elif call.data == 'fifth_poker':
        pass

    elif call.data == 'back_poker':
        index = [n for n, x in enumerate(active_index) if x[:1] == [call.message.chat.id]]
        index = index.pop(0)
        if active_index[index][1] > 0:
            active_index[index][1] -= 5
            poker.send_poker_games(call, index)

    elif call.data == 'next_poker':
        if len(poker_games) > poker_game_index:
            index = [n for n, x in enumerate(active_index) if x[:1] == [call.message.chat.id]]
            index = index.pop(0)
            active_index[index][1] += 5
            poker.send_poker_games(call, index)


# функция для обработки сообщений пользователей
@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message):
    bot_logic.save_id_user(message)
    bot_logic.save_user_message(message)
    profile = [n for n, x in enumerate(profiles) if x[:1] == [message.from_user.id]]
    if not profile:
        profiles.append(
            [
                message.from_user.id,
                Profile(message)
            ]
        )

    if message.text == "Blackjack":
        blackjack.send_offline_blackjack_message(message.from_user.id)

    elif message.text == "Правила покера":
        bot.send_message(
            message.from_user.id,
            config.poker_rules,
            reply_markup=bot_logic.do_leave_markup()
        )

    elif message.text == "Правила Blackjack":
        bot.send_message(
            message.from_user.id,
            config.blackjack_rules,
            reply_markup=bot_logic.do_leave_markup()
        )

    elif message.text == "В главное меню":
        bot.send_message(
            message.from_user.id,
            config.main_menu,
            reply_markup=bot_logic.do_main_markup()
        )

    elif message.text == "Покер":
        bot_logic.send_poker_message(message.from_user.id)

    elif message.text == "Профиль":
        bot_logic.send_profile_message(message.from_user.id)

    elif message.text == "Что умеет бот?":
        bot.send_message(
            message.from_user.id,
            config.bot_functions,
            reply_markup=bot_logic.do_leave_markup()
        )

    else:
        bot.send_message(
            message.from_user.id,
            "Я вас не понимаю...\nИспользуйте меню под строкой сообщения",
            reply_markup=bot_logic.do_leave_markup()
        )


def start_bot():
    if not os.path.exists(os.path.join(os.getcwd(), 'users')):
        os.mkdir(os.path.join(os.getcwd(), 'users'))
        with open(
            'users/ids.data',
            'w',
            encoding='utf-8'
        ) as f:
            f.write(config.dev_info)
    if not os.path.exists(os.path.join(os.getcwd(), 'profiles')):
        os.mkdir(os.path.join(os.getcwd(), 'profiles'))
    print('Бот запустился')
    try:
        bot.infinity_polling()
    except telebot.apihelper.ApiTelegramException as e:
        bot.send_message(
            config.dev_id,
            str(e)
        )
    except IOError as er:
        bot.send_message(
            config.dev_id,
            str(er)
        )


def write_confirm(status: str):
    with open(
            "confirm",
            'w',
            encoding='utf-8'
    ) as confirm:
        confirm.write(status)


def send_start_stop_bot_message(string: str, option: bool = False):
    markup = telebot.types.ReplyKeyboardRemove()
    if option:
        markup = bot_logic.do_leave_markup()
    for id_of_users in bot_logic.get_ids():
        try:
            bot.send_message(
                id_of_users,
                string,
                reply_markup=markup
            )
        except telebot.apihelper.ApiTelegramException as e:
            bot.send_message(
                config.dev_id,
                str(e) + '\n\nID: ' + str(id_of_users)
            )


# бесконечное обновление данных чатов бота
if __name__ == '__main__':
    print("Бот был перезапущен, или ты что-то изменил?\n(напоминаю, 1 - перезапущен, 0 - изменил, 2 - ничего не "
          "посылать): ")
    answer = int(input())
    if answer == 0:
        send_start_stop_bot_message(config.editions, True)
        write_confirm('1')
    elif answer == 1:
        send_start_stop_bot_message(config.rebuild, True)
        write_confirm('1')
    elif answer == 2:
        write_confirm('0')
    try:
        start_bot()
    finally:
        with open(
                "confirm",
                'r',
                encoding='utf-8'
        ) as file:
            if int(file.read()):
                send_start_stop_bot_message(config.closing)
