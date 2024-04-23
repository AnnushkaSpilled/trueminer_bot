import telebot
import logic
import vv

bot_token = vv.bot_token
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f"Привет! Я бот, который поможет тебе записывать доходы и расходы артели Рантье.\n"
                                      f"Выбери команду /tip и я расскажу как добавить запись об операции\n"
                                      f"Команды /last_ten_out и /last_ten_in вызывают последние 10 записей о доходе или расходе соответственно и дают возможность удалить запись")


@bot.message_handler(commands=['in'])
def handle_in_categories(message):
    income_cat = logic.call_lists('income_cat')
    answer = f"Категории доходов\n\n"
    for i in income_cat:
        answer += f"{i[0]} "
        answer += f"{i[1]}\n"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['out'])
def handle_out_categories(message):
    outcome_cat = logic.call_lists('outcome_cat')
    answer = f"Категории расходов\n\n"
    for i in outcome_cat:
        answer += f"{i[0]} "
        answer += f"{i[1]}\n"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['projects'])
def handle_projects(message):
    project = logic.call_lists('project')
    answer = f"Проекты\n\n"
    for i in project:
        answer += f"{i[0]} "
        answer += f"{i[1]}\n"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['last_ten_out'])
def handle_last_ten(message):
    last_ten_list = logic.call_last_ten('out')
    answer = f"Последние 10 записей о расходах в порядке добавления\n\n"
    for i in last_ten_list:
        item = str(i)
        pretty_item = item.replace("'", '').replace('(', '').replace(')', '').replace(',', '')
        answer += f"{pretty_item} /outdel{i[0]}\n"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['last_ten_in'])
def handle_last_ten(message):
    last_ten_list = logic.call_last_ten('in')
    answer = f"Последние 10 записей о доходах в порядке добавления\n\n"
    for i in last_ten_list:
        item = str(i)
        pretty_item = item.replace("'", '').replace('(', '').replace(')', '').replace(',', '')
        answer += f"{pretty_item} /indel{i[0]}\n"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(func=lambda message: message.text.startswith('/outdel'))
def del_expense(message):
    row_id = int(message.text[7:])
    logic.delete_row("out", row_id)
    answer_message = f"Удалил расход {row_id}"
    bot.send_message(message.chat.id, answer_message)


@bot.message_handler(func=lambda message: message.text.startswith('/indel'))
def del_expense(message):
    row_id = int(message.text[6:])
    logic.delete_row("in", row_id)
    answer_message = f"Удалил доход {row_id}"
    bot.send_message(message.chat.id, answer_message)


@bot.message_handler(commands=['tip'])
def handle_tip(message):
    bot.send_message(message.chat.id, "Чтобы добавить доход или расход, отправь мне сообщение в формате:\n"
                                      "0 1 - 2 2500\n"
                                      "Где:\n"
                                      "1 число это маркер даты ('0' если дата операции сегодня, '-1' - вчера, '-2' - позавчера и т.д.)\n\n"
                                      "2 число это идентификатор проекта. Список проектов /projects\n\n"
                                      "3 символ это знак операции (доход или расход)\n\n"
                                      "4 число это идентификатор статьи дохода или расхода. Список статей доходов /in, статей расходов /out\n\n"
                                      "5 число это сумма операции")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        parsed_data = logic.parse_message(message)
        print(parsed_data)
        answer_message = logic.rec_message(parsed_data)
        print(answer_message)
        bot.send_message(message.chat.id, answer_message)
    except (logic.WrongMsgError, logic.WrongProject, logic.WrongCategory) as e:
        bot.send_message(message.chat.id, str(e))


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)