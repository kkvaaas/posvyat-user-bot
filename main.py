import threading
import time
import telebot
from table_parser import mailing, get_user_id, get_user_tag, get_registration, get_data, get_transfer, get_living
import os
from dotenv import load_dotenv


load_dotenv()  # загружает переменные из .env

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
admin_ids = [550509099, 1628109575, 766749758, 2086166118, 1072196201, 847536529]
faq_id = -4570130952

hi_message = 'Привет 💥\nЭто бот Посвящения в студенты 2024\nЗдесь ты будешь получать важную информацию о нашем мероприятии 🤠\nДо встречи в Клондайке🌵\nЧтоб задать вопрос напиши /help'
reg_message = 'Поздравляю! \nТы успешно прошел(а) регистрацию на самое незабываемое событие студенчества 🏜'
transfer_message = 'По коням 🐴\nТы успешно прошел(а) регистрацию на трансфер.'
living_message = 'Выспаться сможешь 🛌 \nТы зарегистрировался(ась). На Посвяте хорошо отдохнешь после захватывающей программы.'
# money_message = 'Оплата прошла успешно'


def add_user(message):
    user_id, user_tag = message.from_user.id, message.from_user.username
    if get_user_id(user_tag) == 0:
        with open('users.txt', 'a') as file:
            file.writelines(str(user_tag) + ' ' + str(user_id) + '\n')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # print(message)
    if message.chat.type == 'private':
        if message.text[0] == '/':
            if message.text == '/start':
                bot.send_message(message.from_user.id, hi_message)
                add_user(message)
            elif message.text == '/help':
                bot.send_message(message.from_user.id, "Задай свой вопрос (для отмены напиши назад)")
                bot.register_next_step_handler(message, get_help)
            else:
                a = message.text.strip().split()
                if a[0] == '/send_message' and message.from_user.id in admin_ids:
                    bot.send_message(message.from_user.id, 'введите название таблицы(для отмены рассылки напишите стоп)')
                    bot.register_next_step_handler(message, get_table)
                else:
                    bot.send_message(message.from_user.id, 'Неизвестная команда')

        else:
            bot.send_message(message.from_user.id, "Для помощи напишите /help")


def get_table(message):
    table_name = message.text
    bot.send_message(message.from_user.id, "введите название поля")
    if message.text.lower().strip() != 'стоп':
        bot.register_next_step_handler(message, get_row, table_name)
    else:
        bot.send_message(message.from_user.id, 'диалог прерван')
        return


def get_row(message, table_name):
    row_name = message.text
    bot.send_message(message.from_user.id, "введите значение поля")
    if message.text.lower().strip() != 'стоп':
        bot.register_next_step_handler(message, get_value, table_name, row_name)
    else:
        bot.send_message(message.from_user.id, 'диалог прерван')
        return


def get_value(message, table_name, row_name):
    row_value = message.text
    bot.send_message(message.from_user.id, "введите отправляемый текст")
    if message.text.lower().strip() != 'стоп':
        bot.register_next_step_handler(message, start_mailing, table_name, row_name, row_value)
    else:
        bot.send_message(message.from_user.id, 'диалог прерван')
        return


def start_mailing(message, table_name, row_name, value):
    txt = message.text
    if table_name and row_name and value and txt:
        try:
            users, warn = mailing(table_name, row_name, value, txt)
        except:
            bot.send_message(message.from_user.id, 'Ошибка рассылки')
        else:
            for user in users:
                user_tag, user_id = user
                try:
                    bot.send_message(user_id, txt)
                except:
                    warn.append((user_tag, user_id))
            if len(users) != 0:
                bot.send_message(message.from_user.id, 'Рассылка совершена')
            else:
                bot.send_message(message.from_user.id, 'Рассылка никому не дошла')
            unreg_mess = ''
            for i in warn:
                unreg_mess += f'@{i[0]}\n'
            bot.send_message(message.from_user.id, 'Не зашли в бота(или неправильно указали тгшку): \n' + unreg_mess)
    else:
        bot.send_message(message.from_user.id, 'Ошибка рассылки')


def get_help(message):
    if message.text.lower().strip() != 'назад':
        user_tag = get_user_tag(message.from_user.id)
        if user_tag:
            bot.send_message(faq_id, f'message from user @{get_user_tag(message.from_user.id)}\n' + message.text)
            bot.send_message(message.from_user.id, 'Спасибо за вопрос жди ответа')
        else:
            bot.send_message(message.from_user.id, 'Произошла ошибка, напиши еще раз')
    else:
        bot.send_message(message.from_user.id, 'Диалог прерван')
        return


def send_periodic_messages():
    while True:
        data = get_data('Registration')
        users_tag = get_registration(data)
        for user_tag in users_tag:
            try:
                bot.send_message(get_user_id(user_tag), reg_message)
            except:
                pass
            else:
                with open('reg_list.txt', 'a') as file:
                    file.writelines(str(user_tag) + '\n')

        data = get_data('Transfer')
        users_tag = get_transfer(data)
        for user_tag in users_tag:
            try:
                bot.send_message(get_user_id(user_tag), transfer_message)
            except:
                pass
            else:
                with open('transfer_list.txt', 'a') as file:
                    file.writelines(str(user_tag) + '\n')

        data = get_data('Rasselenie')
        users_tag = get_living(data)
        for user_tag in users_tag:
            try:
                bot.send_message(get_user_id(user_tag), living_message)
            except:
                pass
            else:
                with open('living_list.txt', 'a') as file:
                    file.writelines(str(user_tag) + '\n')
        time.sleep(300)


thread = threading.Thread(target=send_periodic_messages)
thread.start()
bot.polling(none_stop=True, interval=0)
