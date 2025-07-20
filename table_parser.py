import gspread
json_file = 'bot_auth.json'
gc = gspread.service_account(filename=json_file)
sh = gc.open('second')

name_tg_cell = 'TG'


def mailing(table_name, row, value, mess):
    users = []
    warn = []
    if table_name and row and value and mess:
        worksheet = sh.worksheet(table_name)
        a = worksheet.get_all_records()
        for cell in a:
            if value == str(cell[row]):
                user_tag = cell[name_tg_cell].replace('@', '')
                user_id = get_user_id(user_tag)
                if user_id:
                    users.append((user_tag, user_id))
                else:
                    warn.append((user_tag, user_id))
    return users, warn


def get_data(table_name: str):
    worksheet = sh.worksheet(table_name)
    return worksheet.get_all_records()


def get_registration(a):
    users = []
    with open('reg_list.txt') as file:
        reg_users = file.read().split('\n')
    for cell in a:
        user_tag = cell[name_tg_cell].replace('@', '')
        if user_tag not in reg_users:
            users.append(user_tag)

    return users

def get_transfer(a):
    users = []
    with open('transfer_list.txt') as file:
        reg_users = file.read().split('\n')
    for cell in a:
        user_tag = cell[name_tg_cell].replace('@', '')
        if user_tag not in reg_users:
            users.append(user_tag)

    return users


def get_living(a):
    users = []
    with open('living_list.txt') as file:
        reg_users = file.read().split('\n')
    for cell in a:
        user_tag = cell[name_tg_cell].replace('@', '')
        if user_tag not in reg_users:
            users.append(user_tag)

    return users

def get_user_id(user_tag: str):
    user_id = 0
    with open('users.txt') as f:
        data = f.read().split('\n')
        for i in data:
            try:
                tag, tag_id = i.split()
                tag_id = int(tag_id)
                if tag == user_tag:
                    user_id = tag_id
                    break
            except:
                break
    return user_id


def get_user_tag(user_id: int):
    user_name = ''
    with open('users.txt') as f:
        data = f.read().split('\n')
        for i in data:
            try:
                tag, tag_id = i.split()
                tag_id = int(tag_id)
                if tag_id == user_id:
                    user_name = tag
                    break
            except:
                break
    return user_name
