import telebot
from config import token

# инициализация бота и его привязка к телеграму
bot = telebot.TeleBot(token)

poker_games = []
"""
список активных покер игр
структура списка:
[
  [
    game_id,
    [
      [
        active_user_id,
        Hand(),
        dealer_status,
        money,
        bet
      ],
      ...
    ],
    bank,
    stack, ///или начальное кол-во фишек
    Cards()
  ],
  ...
]
"""

active_index = []
"""
Переменная для хранения активных индексов пользователей:
структура:
[
    [
       ид пользователя,
       его индекс списка,
       сообщение бота
    ],
    ...
]
"""

offline_blackjack_games = []
"""
список активных оффлайн Blackjack игр
структура списка:
[
  [
    id_user
    Hand(),
    Cards(),
    BotBlackjack()
    bot_message,
    bet
  ],
  ...
]
"""

online_blackjack_games = []
"""
список активных онлайн Blackjack игр
структура списка:
[
  [
    [
      [
        active_user_id,
        Hand()
      ],
      ...
    ]
    Cards(),
    bot_message
  ],
  ...
]
"""

profiles = []
"""
список пользователей с их id
структура:\n
[\n
[\n
user_id: int\n
user: Profile\n
],\n
...\n
]
"""

profile_messages = []
"""
список сообщений пользователей\n
структура:\n
[\n
[\n
user_id: int\n
bot_message\n
],\n
...\n
]
"""
