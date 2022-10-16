from telebot import types

import config
from variables import poker_games, active_index, bot
from classes import Hand, Cards
import bot_logic

poker_game_index = 0
"""
Индекс созданных игр
"""


def get_poker_game(game_index: int):
    poker_game = [n for n, x in enumerate(poker_games) if x[:1] == [game_index]]
    if poker_game:
        return poker_games[poker_game.pop(0)]
    else:
        return None


def connect_to_poker_game(gamer_index: int, game_index: int):

    pass


def create_poker_game(call: types.CallbackQuery, stack):
    for i in poker_games:
        game = [n for n, x in enumerate(i[1]) if x[:1] == [call.message.chat.id]]
        if game:
            bot.send_message(
                call.message.chat.id,
                config.create_poker_exist,

            )
    global poker_game_index
    poker_games.append(
        [
            poker_game_index,
            [
                [
                    call.message.chat.id,
                    Hand(),
                    False
                ]
            ],
            0,
            stack,
            Cards()
        ]
    )
    poker_game_index += 1


def send_poker_games(call: types.CallbackQuery, index: int):
    """Функция по отправки сообщения с выбором покер игры для подключения"""
    poker_string = 'Список активных игр:\n'
    j = 1
    for i in poker_games[active_index[index][1]:active_index[index][1]+5]:
        poker_string += str(active_index[index][1] + j) + '. Количество игроков: ' + str(len(i[1])) + \
                        '/5\nРазмер стека: ' + str(i[3]) + '-' + str(i[4])
        j += 1
    if '1.' in poker_string:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=active_index[index][2].message_id,
            text=poker_string,
            reply_markup=bot_logic.do_poker_list_markup(index)
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text="Нет доступных игр...",
            message_id=active_index[index][2].message_id,
            reply_markup=bot_logic.do_poker_menu_markup()
        )
