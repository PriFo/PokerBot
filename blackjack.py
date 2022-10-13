import random
from time import sleep

import config
from classes import Hand, Cards, BotBlackjack
from variables import offline_blackjack_games, profiles, bot
from telebot import types
import bot_logic


def check_cards(cards: list, summary_bot: int):
    need_to_win = 21 - summary_bot
    count_of_ok = 0
    count_of_all = len(cards)
    for i in cards:
        if i.value > 10:
            if 10 <= need_to_win:
                count_of_ok += 1
        elif i.value <= need_to_win:
            count_of_ok += 1
    chance = count_of_ok / count_of_all
    return chance


def save_blackjack_bet(user_id: int, hand_user: list):
    hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [user_id]]
    if len(hand) > 1:
        hand = hand.pop(1)
        bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=offline_blackjack_games[hand][4].message_id,
            reply_markup=None
        )
        offline_blackjack_games.pop(hand)
        hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [user_id]]
    offline_blackjack_games.pop(hand.pop())
    bot.edit_message_text(
        chat_id=user_id,
        message_id=hand_user[4].message_id,
        text="Ваша ставка: " + str(hand_user[5]) + " у.е.",
        reply_markup=bot_logic.do_blackjack_bet_markup()
    )
    offline_blackjack_games.append(hand_user)


# функция для демонстрации руки в Blackjack
def show_hand_blackjack(id_user: int):
    hand_str = "Ваша рука: "
    hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [id_user]]
    if hand:
        hand = offline_blackjack_games[hand.pop(0)][1].cards
        summary = 0
        for i in hand:
            hand_str += bot_logic.get_string_card(i)
            if i.value == 1:
                if (21 - summary) >= 11:
                    summary += 11
                else:
                    summary += 1
            elif i.value >= 10:
                summary += 10
            else:
                summary += i.value
        if summary:
            hand_str += "\nСумма вашей руки: " + str(summary)
        else:
            hand_str += "Пусто\nВозьмите карту"
        if summary < 21:
            return hand_str
        elif summary > 21:
            hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [id_user]]
            offline_blackjack_games.pop(hand.pop())
            return hand_str + "\nВы проиграли😞"
        else:
            hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [id_user]]
            offline_blackjack_games.pop(hand.pop())
            return hand_str + "\nВы выиграли😃"


def send_offline_blackjack_message(user_id: int):
    hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [user_id]]
    if not hand:
        bot.send_message(
            user_id,
            "Запуск игры...",
            reply_markup=types.ReplyKeyboardRemove()
        )
        sleep(0.5)
        index_profile = [n for n, x in enumerate(profiles) if x[:1] == [user_id]].pop(0)
        user = profiles[index_profile][1]
        if user.money >= 10:
            bet = user.money // 100 * 10 if user.money > 100 else 10
            offline_blackjack_games.append(
                [
                    user_id,
                    Hand(),
                    Cards(),
                    BotBlackjack(),
                    bot.send_message(
                        user_id,
                        "Ваша нынешняя ставка: " + str(bet) + " у.е.",
                        reply_markup=bot_logic.do_blackjack_bet_markup()
                    ),
                    bet
                ]
            )
        else:
            bot.send_message(
                user_id,
                "Вы не можете начать игру\n",
                reply_markup=bot_logic.do_main_markup()
            )


def set_bet(message: types.Message):
    user = [n for n, x in enumerate(profiles) if x[:1] == [message.from_user.id]].pop(0)
    user = profiles[user][1]
    hand_user = get_hand(message.from_user.id)
    if bot_logic.check_int([message.text]):
        if user.money < int(message.text):
            hand_user[5] = user.money
        elif int(message.text) <= 10:
            hand_user[5] = 10
        else:
            hand_user[5] = int(message.text)
        save_blackjack_bet(message.from_user.id, hand_user)
    else:
        save_blackjack_bet(message.from_user.id, hand_user)


def change_bet_blackjack(call: types.CallbackQuery, option: int):
    """
    option_1 = raise_bet\n
    option_2 = lower_bet\n
    option_3 = max_bet\n
    option_4 = min_bet\n
    option_5 = set_bet\n
    """
    index_profile = [n for n, x in enumerate(profiles) if x[:1] == [call.message.chat.id]]
    if index_profile:
        index_profile = index_profile.pop(0)
        user = profiles[index_profile][1]
        hand_user = get_hand(call.message.chat.id)
        if hand_user:
            if option == 1:
                if not user.money == hand_user[5]:
                    hand_user[5] *= 2
                    if user.money < hand_user[5]:
                        hand_user[5] = user.money
                    save_blackjack_bet(call.message.chat.id, hand_user)
            elif option == 2:
                if not hand_user[5] == 10:
                    hand_user[5] //= 2
                    if hand_user[5] < 10:
                        hand_user[5] = 10
                    save_blackjack_bet(call.message.chat.id, hand_user)
            elif option == 3:
                if not user.money == hand_user[5]:
                    hand_user[5] = user.money
                    save_blackjack_bet(call.message.chat.id, hand_user)
            elif option == 4:
                if not hand_user[5] == 10:
                    hand_user[5] = 10
                    save_blackjack_bet(call.message.chat.id, hand_user)
            elif option == 5:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Введите вашу ставку (не более " + str(user.money) + " у.е.):",
                    message_id=hand_user[4].message_id
                )
                bot.register_next_step_handler(hand_user[4], set_bet)


def get_hand(user_id: int):
    hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [user_id]]
    if hand:
        return offline_blackjack_games[hand.pop(0)]
    else:
        return None


def take_card(call: types.CallbackQuery):
    hand_user = get_hand(call.message.chat.id)
    if hand_user:
        hand_user[1].cards.append(hand_user[2].cards.pop(random.randint(0, len(hand_user[2].cards) - 1)))
        result = str(show_hand_blackjack(call.message.chat.id))
        if "Вы проиграли" not in result and "Вы выиграли" not in result:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=hand_user[4].message_id,
                text=result,
                reply_markup=bot_logic.do_blackjack_markup()
            )
        else:
            index_profile = [n for n, x in enumerate(profiles) if x[:1] == [call.message.chat.id]].pop(0)
            user = profiles[index_profile][1]
            if "Вы выиграли" in result:
                user.blackjack_wins += 1
                user.money += hand_user[5]
            else:
                user.money -= hand_user[5]
            user.blackjack_games += 1
            user.save_profile()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=hand_user[4].message_id,
                text=result,
            )
            bot.send_message(
                call.message.chat.id,
                config.main_menu,
                reply_markup=bot_logic.do_main_markup()
            )


def hold_cards(call: types.CallbackQuery):
    hand_user = get_hand(call.message.chat.id)
    index_profile = [n for n, x in enumerate(profiles) if x[:1] == [call.message.chat.id]].pop(0)
    user = profiles[index_profile][1]
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=hand_user[4].message_id,
        reply_markup=None
    )
    if hand_user:
        summary_bot = 0
        summary = 0
        for i in hand_user[1].cards:
            if i.value == 1:
                if (21 - summary) >= 11:
                    summary += 11
                else:
                    summary += 1
            elif i.value >= 10:
                summary += 10
            else:
                summary += i.value
        bot_message = bot.send_message(
            call.message.chat.id,
            "Дилер начинает брать карты"
        )
        sleep(1)
        bot_cards = ""
        while True:
            bot_str = "Рука дилера: "
            card = hand_user[2].cards.pop(random.randint(0, len(hand_user[2].cards) - 1))
            hand_user[3].hand.cards.append(card)
            bot_cards += bot_logic.get_string_card(card)
            if card.value == 1:
                if (21 - summary_bot) >= 11:
                    summary_bot += 11
                else:
                    summary_bot += 1
            elif card.value >= 10:
                summary_bot += 10
            else:
                summary_bot += card.value
            bot_str += bot_cards + "\nСумма руки диллера: " + str(summary_bot)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=bot_message.message_id,
                text=bot_str
            )
            sleep(1)
            if check_cards(hand_user[2].cards, summary_bot) < 0.35:
                break
            elif summary < summary_bot:
                break
        if summary_bot == 21:
            user.blackjack_games += 1
            user.money -= hand_user[5]
            user.save_profile()
            bot.send_message(
                call.message.chat.id,
                'Вы проиграли😞',
                reply_markup=bot_logic.do_main_markup()
            )
        elif summary_bot > 21:
            user.blackjack_wins += 1
            user.money += hand_user[5]
            user.blackjack_games += 1
            user.save_profile()
            bot.send_message(
                call.message.chat.id,
                'Вы выиграли😃',
                reply_markup=bot_logic.do_main_markup()
            )
        elif summary_bot > summary:
            user.blackjack_games += 1
            user.money -= hand_user[5]
            user.save_profile()
            bot.send_message(
                call.message.chat.id,
                'Вы проиграли😞',
                reply_markup=bot_logic.do_main_markup()
            )
        elif summary_bot == summary:
            user.blackjack_games += 1
            user.save_profile()
            bot.send_message(
                call.message.chat.id,
                'Ничья👍',
                reply_markup=bot_logic.do_main_markup()
            )
        else:
            user.blackjack_wins += 1
            user.blackjack_games += 1
            user.money += hand_user[5]
            user.save_profile()
            bot.send_message(
                call.message.chat.id,
                'Вы выиграли😃',
                reply_markup=bot_logic.do_main_markup()
            )
        hand = [n for n, x in enumerate(offline_blackjack_games) if x[:1] == [call.message.chat.id]]
        offline_blackjack_games.pop(hand.pop())
