VPN BOT. V1.2

------------------------------------------------------------------------------------------------------

Навигатор в коде:

requirements.txt - Файл с нужными библиотеками.
REAME.md - ТЫ здесь.
main.py - Этот файл отвечает за запуск бота и проверку подписки у пользователей.
conf.py - !В этом файле создерэжится все данные которые требуются для работы бота, телеграм токен бота, токен Outline и токен магазина, через который вы будете производить оплату.
bot_users.db - БАЗА ДАННЫХ БОТА, ДОЛЖЕН БЫТЬ ФАЙЛ, НЕ УДАЛЯТЬ.

Папка app в которой содержися сам бот и его функционал.
app/router.py - Этот файл отвечает за работу и функционал бота.
app/keyboards.py - Этот файл отвечает за клавиатуру бота.

------------------------------------------------------------------------------------------------------

Для запуска бота.

1. Открыть cmd в папке с ботом, и прописать команду
pip install -r requirements.txt

2. Указать свои данные в файле conf.py

3. Запустить файл main.py шелчком мышки или командой python main.py

------------------------------------------------------------------------------------------------------

Фукнционал?
1. Профиль, инва о пользователе, его id, Имя, Токен, Срок дейвствия впн токена и локальное время в боте.

2. Инфо о токене, показывает урезанную версию инфы того что в ПРОФИЛЕ

3. Купить VPN, оплата производится через телеграм и его поддерживаемые способы оплаты, ЮКАССА, СБЕРБАНК, РОБОКАССА и некоторое другое. Полный список можно посмотреть в боте.
"@BotFather -> /mybots -> твой_бот -> payments ->"

4. Поддержка, тут вы можете указать свой бот для свзяи, или контакт.