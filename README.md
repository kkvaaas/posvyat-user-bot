# Сервисный аккаунт будет в гит игноре, при деплое создадим какой то общий сервисный аккаунт

Что бы создать аккаунт для работы и теста - инструкция ниже

полученный .json назвать bot_auth.json

так же токен бота будем брать из .env файла, его тоже закинул в гит игнор

#Пример .env ФАЙЛА
```
TOKEN="token_here"
GSHEET_CREDS_PATH="bot_auth.json"
GSHEET_NAME="hsebot"
```
# Если какие то вопросы по этому что я написал пишите в тг @egorikkfn


# запуск :
```
docker build -t mybot:latest .    
docker run -d --name posvyat_container  mybot:latest 
```
# Создание сервисного аккаунта
✅ Шаг 1: Создание проекта (если ещё нет)

Перейди на Google Cloud Console.

В правом верхнем углу выбери или создай новый проект.

Назови его, например: telegram-bot-project.

✅ Шаг 2: Включение Google Sheets API
В меню слева перейди в: APIs & Services → Library.

Найди и включи:

Google Sheets API

Google Drive API (нужен для доступа к файлу по имени)

✅ Шаг 3: Создание сервисного аккаунта
Перейди в: APIs & Services → Credentials.

Нажми кнопку: “+ CREATE CREDENTIALS” → “Service account”.

Назови его, например: telegram-bot-access.

Нажми "Create and continue".

🔒 На этапе "Role" можешь выбрать:

Editor — если нужен полный доступ.

Или ничего не выбирать (будет достаточно).

Нажми “Done”.

✅ Шаг 4: Создание ключа (JSON-файла)
После создания аккаунта ты попадёшь на список сервисных аккаунтов.

Найди нужный → нажми на имя → вкладка “Keys”.

Нажми: “Add Key” → “Create new key” → JSON.

Скачается .json файл (пример: telegram-bot-access-8d9c33e9.json).

📁 Положи этот файл в корень проекта и переименуй, например, в:
bot_auth.json
✅ Шаг 5: Дать доступ к таблице
Открой нужную Google таблицу (Google Sheets).

Нажми "Поделиться" (Share).

В поле "Добавить пользователей" вставь email из JSON-файла, он выглядит так:


telegram-bot-access@telegram-bot-project.iam.gserviceaccount.com
Назначь Editor (редактор), нажми "Отправить".
