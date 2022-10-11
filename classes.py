from random import shuffle

from telebot import types

from variables import bot


class BotBlackjack:
    """Класс, хранящий руку бота для игры в Blackjack"""

    def __init__(self):
        self.hand = Hand()


class Card:
    """Класс, хранящий информацию о конкретной карте"""

    def __init__(self, value: int, suit: int):
        self.value = value
        self.suit = suit


class Cards:
    """Класс, хранящий информацию о колоде карт"""

    def __init__(self):
        self.cards = []
        for i in range(1, 4):
            for j in range(1, 13):
                card = Card(j, i)
                self.cards.append(card)
        shuffle(self.cards)


class Hand:
    """Класс, хранящий информацию о руке игроков (подходит как для покера, так и для Blackjack)"""

    def __init__(self):
        self.cards = []


class Profile:
    """Класс, хранящий информацию о профилях пользователей, а также содержит методы обработки пользовательской
    информации """

    def __init__(self, message: types.Message):
        self.user_id = message.from_user.id
        self.name = message.from_user.username
        self.money = 10000
        self.blackjack_games = 0
        self.blackjack_wins = 0
        self.bonus_date = "2012-1-1"
        try:
            with open(
                    'profiles/' + str(self.user_id) + ".data",
                    'r+',
                    encoding='utf-8'
            ) as f:
                for i in range(0, 5):
                    chunk = f.readline()
                    if i == 0:
                        self.name = str(chunk)
                        self.name = self.name.replace("\n", "")
                    elif i == 1:
                        self.money = int(chunk)
                    elif i == 2:
                        self.bonus_date = str(chunk)
                        self.bonus_date = self.bonus_date.replace("\n", "")
                    elif i == 3:
                        self.blackjack_games = int(chunk)
                    elif i == 4:
                        self.blackjack_wins = int(chunk)
        except IOError:
            self.save_new_profile(message)
            bot.send_message(
                self.user_id,
                "Вам был присвоен новый профиль, так как он еще не заведен, либо был сброшен"
            )

    def get_string(self):
        profile_string = "Здравствуйте, " + str(self.name) + "!\nВаш баланс: " + str(self.money) + "\nBlackjack игр " \
                                                                                                   "сыграно: " + str(
            self.blackjack_games) + "\nBlackjack игр выиграно: " + str(self.blackjack_wins)
        return profile_string

    def save_profile(self):
        with open(
                'profiles/' + str(self.user_id) + ".data",
                'w',
                encoding='utf-8'
        ) as f:
            f.write(str(self.name) + "\n")
            f.write(str(self.money) + "\n")
            f.write(self.bonus_date + "\n")
            f.write(str(self.blackjack_games) + "\n")
            f.write(str(self.blackjack_wins) + "\n")

    def save_new_profile(self, message: types.Message):
        with open(
                'profiles/' + str(self.user_id) + ".data",
                'w+',
                encoding='utf-8'
        ) as f:
            if message.from_user.username is not None:
                f.write(str(message.from_user.username) + "\n")
            else:
                f.write(str(message.from_user.first_name) + "\n")
            f.write(str(10000) + "\n")
            f.write("2012-1-1" + "\n")
            f.write(str(0) + "\n")
            f.write(str(0) + "\n")


class Table:

    def __init__(self, cards: Cards = None, ):
        if cards is None:
            self.cards = Cards()
        else:
            self.cards = cards
        self.community_cards = []

    def get_community_cards(self):
        return self.community_cards

    def get_last_card(self):
        return self.cards.cards.pop()
