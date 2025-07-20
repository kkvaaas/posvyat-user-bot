import gspread
import requests

json_file = 'bot_auth.json'
gc = gspread.service_account(filename=json_file)
sh = gc.open('second')


def get_reg():
    r = requests.get('http://miemposvyat.ru/api/v1/all_registration')
    data = r.json()
    res = []
    for i in data:
        res.append(list(i.values())[1:])
    return res


def main():
    results = get_reg()
    worksheet = sh.worksheet('Registration')
    data = [['Name', 'Surname',	'Middle Name', 'VK', 'TG', 'Phone', 'Birthday', 'Sex', 'University', 'Faculty', 'Group', 'Transfer', 'Course', 'Health Features']]
    for row in results:
        data.append(row)
    print(len(data))
    range_rotation = f'A1:N{len(data)}'
    worksheet.update(data, range_rotation)


main()
# while True:
#     try:
#         main()
#     except:
#         pass
#     sleep(30)

