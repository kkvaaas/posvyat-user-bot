import gspread
from dotenv import load_dotenv
import os

load_dotenv()

json_file = os.getenv("GSHEET_CREDS_PATH")
sheet_name = os.getenv("GSHEET_NAME")
gc = gspread.service_account(filename=json_file)
sh = gc.open(sheet_name)

name_tg_cell = 'TG'


gc = gspread.service_account(filename='bot_auth.json')
sh = gc.open('hsebot')  # имя вашей таблицы
worksheet = sh.worksheet('second')  # нужный лист


def find_user_in_sheet(user_tag: str):
    """
    Ищем пользователя по Telegram username (user_tag с @)
    Возвращаем словарь с данными (Name, Surname, Middle Name и т.п.) или None.
    """
    all_records = worksheet.get_all_records()
    print("123")
    for record in all_records:
        tg_username = record.get('TG', '').strip()
        if tg_username == user_tag:
            return record
    return None



def get_data(table_name: str):
    worksheet = sh.worksheet(table_name)
    return worksheet.get_all_records()


def get_registration(data):
    return get_new_users(data, 'reg_list.txt')


def get_transfer(data):
    return get_new_users(data, 'transfer_list.txt')


def get_living(data):
    return get_new_users(data, 'living_list.txt')


def get_new_users(data, filename):
    with open(f'data/{filename}', 'r') as f:
        known = set(f.read().splitlines())
    users = []
    for cell in data:
        user_tag = cell.get(name_tg_cell, '').replace('@', '')
        if user_tag and user_tag not in known:
            users.append(user_tag)
    return users


def get_user_id(user_tag: str):
    with open('data/users.txt', 'r') as f:
        for line in f:
            try:
                tag, uid = line.strip().split()
                if tag == user_tag:
                    return int(uid)
            except:
                continue
    return 0


def get_user_tag(user_id: int):
    with open('data/users.txt', 'r') as f:
        for line in f:
            try:
                tag, uid = line.strip().split()
                if int(uid) == user_id:
                    return tag
            except:
                continue
    return ''
