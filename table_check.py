import gspread

json_file = 'bot_auth.json'
gc = gspread.service_account(filename=json_file)
sh = gc.open('hsebot')

worksheet = sh.worksheet('second')
a = worksheet.get_all_records()
print(a)