import os
import telebot
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from table_parser import find_user_in_sheet
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = AsyncTeleBot(TOKEN)
admin_ids = [1232239269]

# Заранее загружаем user_id из файла в память
users_dict = {}
if os.path.exists('data/users.txt'):
    with open('data/users.txt', 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                users_dict[parts[0]] = int(parts[1])


def save_user(user_tag, user_id):
    if user_tag not in users_dict:
        users_dict[user_tag] = user_id
        with open('data/users.txt', 'a') as file:
            file.write(f"{user_tag} {user_id}\n")


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(
        InlineKeyboardButton("Регистрация", callback_data="register"),
        InlineKeyboardButton("Задать вопрос", callback_data="help")
    )
    keyboard.add(
        InlineKeyboardButton("FAQ", url="https://t.me/тут url посвята")
    )
    return keyboard


@bot.message_handler(commands=['start'])
async def start_handler(message):
    user_id = message.from_user.id
    user_tag = message.from_user.username

    if not user_tag:
        await bot.send_message(user_id, "Пожалуйста, установи username в Telegram, чтобы использовать бота.")
        return

    save_user(user_tag, user_id)

    user_data = find_user_in_sheet(user_tag)
    if user_data is None:
        await bot.send_message(user_id,
            "Привет! Похоже, ты ещё не зарегистрировался(ась).\n"
            "Пожалуйста, пройди регистрацию на сайте: https://example.com/register\n"
            "После регистрации вернись сюда и нажми /start снова."
        )
    else:
        name = user_data.get('Имя', '')
        surname = user_data.get('Фамилия', '')
        await bot.send_message(user_id, f"Привет, {name} {surname}!\nРады видеть тебя! Если нужна помощь, напиши /help.")


# Callback обработка
@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call):
    if call.data == "register":
        await bot.send_message(call.message.chat.id, "Для регистрации напиши /start и следуй инструкциям.")
    elif call.data == "help":
        await bot.send_message(call.message.chat.id, "Напиши свой вопрос сюда:")
        bot.register_next_step_handler(call.message, get_help)


# Пример функции вопроса
async def get_help(message):
    await bot.send_message(message.chat.id, "Спасибо за вопрос. В скором времени с тобой свяжутся.")


# Основной асинхронный запуск
async def main():
    await bot.polling(non_stop=True)

if __name__ == "__main__":
    asyncio.run(main())
