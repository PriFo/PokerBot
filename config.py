version = '0.4.2'
dev_id = '517965582'
dev_info = '517965582 | pr1fo | Alex | Skrebnev\n'
ask_for_help = 'Version: ' + version + '\n\n' \
                                       'Создатель: @pr1fo\n\n' \
                                       'Что вас интересует?'
blackjack_rules = 'Правила игры в Blackjack (21):\n' \
                  '\t\t○ Игры рассчитана на 2х игроков, в данный момент доступна возможность играть только с дилером ' \
                  '(ботом)\n\n' \
                  '• Что нужно делать?\n\n' \
                  '\t\t○ Цель игры: набрать в сумме 21 очко, причём каждая карта имеет свой вес (цифры 2-10 имеют вес '\
                  '2-10 соответственно, Туз имеет вес 11, но если очков уже больше или равно 11, то туз имеет вес 1, ' \
                  'Валет, Дама и Король имеют вес 10). Масть карты в данном случае значения не имеет. Если на руке ' \
                  'есть 2 туза, то игра заканчивается выигрышем владельца этих тузов (Золотое очко)\n\n' \
                  '\t\t○ Вы начинаете игру: вы можете взять карту, если считаете необходимым, а можете удержать ту ' \
                  'комбинацию, которую имеете. Если вы набираете 21 очко, то вы выигрываете, если же набирает дилер, ' \
                  'то выигрывает он. Если ни один из игроков не набрал 21 очко, то смотрится у кого очков больше, но ' \
                  'если у кого-то очков больше 21 (перебор), то выигрывает его оппонент. '
poker_rules = 'Правила игры в Texas Hold\'em Poker:\n\n' \
              '• Игра начинается, когда в комнате больше 1 игрока;\n' \
              '• Один из игроков становится дилером (в течении игры каждый из игроков станет им);\n' \
              '• Когда игра началась, производятся слепые ставки (малый и большой блайнды(0.5% и 1% от входного ' \
              '• баланса соответственно) двумя людьми слева от дилера (ход по часовой стрелке));\n' \
              '• Каждому игроку выдаётся по 2 карты в руку;\n' \
              '• Начинается приём ставок:\n' \
              '\t\t○ каждый может принять ставку, повысить ставку, либо отказаться от ставки;\n' \
              '\t\t○ приём ставок продолжается до тех пор, пока все не приняли последнее повышение;\n' \
              '\t\t○ если за столом остался 1 игрок, то игра прекращается, а весь накопленный банк идёт 1 игроку;\n' \
              '• После приёма ставок на стол выкладывается флоп (первые 3 карты стола);\n' \
              '• Приём ставок повторяется;\n' \
              '• На стол выкладывается тёрн (4-я карта стола);\n' \
              '• Приём ставок повторяется снова;\n' \
              '• На стол выкладывается ривер (5-я и последняя карта стола);\n' \
              '• Начинается окончательный приём ставок;\n' \
              '• Если за столом осталось больше 1 человека, то начинается сравнивание комбинаций, которые образуются ' \
              '• картами руки и стола (далее от менее к более выгодной):;\n' \
              '\t\t○ Старшая карта (сравнение рук, при этом ни у кого нет других комбинаций);\n' \
              '\t\t○ Пара (две карты одинакового достоинства);\n' \
              '\t\t○ Две пары (две пары карт одинакового достоинства);\n' \
              '\t\t○ Сет (тройка) (три карты одного достоинства);\n' \
              '\t\t○ Стрит (пять последовательно расположенных карт (пример: 2♥, 3♦, 4♣, 5♥, 6♥));\n' \
              '\t\t○ Флеш (пять карт одной масти);\n' \
              '\t\t○ Фулл-хаус (три карты одного достоинства и две карты другого);\n' \
              '\t\t○ Каре (четыре карты одного достоинства);\n' \
              '\t\t○ Стрит-флеш (Стрит, в котором все 5 карт одной масти);\n' \
              '\t\t○ Флеш-рояль (Стрит-флеш от десяти до туза);\n' \
              '• В зависимости от комбинации выбирается победитель, которому выдаётся весь банк, и игра повторяется;\n'\
              '• Если за столом 2 и более выигрышные комбинации, то банк делится поровну между игроками.'
main_menu = 'Вы в главном меню'
all_commands = "/start <None>\n" \
               "/help <None>\n" \
               "/commands <None>\n" \
               "/show_ids <None>\n" \
               "/poker <None>\n" \
               "/active_blackjack <None>\n" \
               "/profile_messages <None>\n" \
               "/message <ids_of_users> : <text>\n" \
               "/log <ids_of_users>"
bot_functions = 'На данный момент бот умеет:\n\t' \
                '• проводить Blackjack игры с ботом;\n\t' \
                '• предоставлять взаимодействие с профилем\n\t' \
                '• предоставлять правила игр, которые ныне реализованы\n\n' \
                'В планах для реализации:\n\t' \
                '• проведение техасских покер-игр с другими игроками\n\t' \
                '• вывод статистики по различным играм\n\t' \
                '• проведение Blackjack игр с другими игроками\n\t' \
                '• отправка идей, предложений и возможных технических сбоев бота'
editions = 'Бот был обновлён:\n\t\t' \
           '• были внесены небольшие изменения в бота.\n\t\t' \
           '• было добавлено \"Золотое очко\" в Blackjack.\n\n' \
           'Данная версия: ' + version
rebuild = 'Бот был перезапущен, вся не сохранённая информация была сброшена. Приношу извинения за все косяки'
closing = "Бот выключился на технический перерыв, приношу извинения за неудобства"
create_poker_exist = 'Вы не можете создать игру, так как вы уже подключены к другой'
connect_to_another_poker = 'Вы подключены к другой игре, сначала отключитесь от прошлой'