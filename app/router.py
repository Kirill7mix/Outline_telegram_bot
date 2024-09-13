import sqlite3 # База данных.
from conf import api_url, cert_sha256, PAYMENTS_PROVIDER_TOKEN
from aiogram import Bot, Dispatcher, F, Router, types #AIOGRAM????
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup #AIOGRAM????
from aiogram.methods import SendInvoice, AnswerPreCheckoutQuery #AIOGRAM????
from aiogram.types import Message, CallbackQuery #AIOGRAM????
from aiogram.filters import CommandStart #AIOGRAM????
from datetime import datetime, timedelta #Время
import requests # Работа с запросами, вроде не используется хз можно убрать
import os #Работа с файлами.
import time #Время, но другое
from aiogram.types import FSInputFile # Модуль для отправки файлов
from colorama import Fore, Back, Style, init # Более чёткий вывод инфо работы бота.
from outline_vpn.outline_vpn import OutlineVPN # API outline, нсколько я помню, не официальное.
import app.keyboards as kb # Клавиатура бота

client = OutlineVPN(api_url=api_url, cert_sha256=cert_sha256)

router = Router()

# Функция для получения данных о текущей подписке. Точнее её годность.
def check_subscription(user_id: int):
    conn = sqlite3.connect('bot_users.db')  # Подключение к базе данных
    cursor = conn.cursor()
    
    # Запрос для получения даты окончания подписки
    cursor.execute("SELECT vpn_expiration FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result and result[0]:
        vpn_expiration = result[0]
        # Преобразуем строку с датой в объект datetime
        vpn_expiration_date = datetime.strptime(vpn_expiration, '%Y-%m-%d %H:%M:%S')
        
        # Сравниваем дату окончания подписки с текущей датой
        if vpn_expiration_date > datetime.now():
            return vpn_expiration_date
    
    return None

@router.message(CommandStart())
async def check(message: Message):
    # Подключение к базе данных
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    # Обновление структуры таблицы.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        date_registration TEXT,
        vpn_token TEXT,
        vpn_expiration TEXT,
        key_id TEXT
    )
    ''')

    # Проверяем, есть ли столбец key_id в таблице, и если нет, то добавляем его
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'key_id' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN key_id TEXT")

    conn.commit()

    user_id = message.from_user.id
    user_name = message.from_user.full_name

    key_id= f"New{message.from_user.id} key"

    # SQL-запрос для поиска пользователя в базе данных
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()  # Получаем первую строку результата запроса

    if user:
        await message.answer("Приветствуем!", reply_markup=kb.main)
        print(f"{Fore.LIGHTYELLOW_EX}Прожали старт. {Style.RESET_ALL}{datetime.now()}")
        # Здесь можно добавить логику для показа информации о пользователе
    else:
        # Если пользователя нет, добавляем его в базу данных
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO users (id, name, date_registration, key_id) VALUES (?, ?, ?, ?)", 
                       (user_id, user_name, registration_date, key_id))
        conn.commit()
        await message.answer(
            f"Приветствуем!\n<tg-spoiler>Вы были добавлены в базу данных.</tg-spoiler>",
            reply_markup=kb.main,
            parse_mode='HTML'
        )

        print(f"{Fore.LIGHTYELLOW_EX}Новый пользователь! {Style.RESET_ALL}{datetime.now()}")
    
    # Закрытие соединения с базой данных
    conn.close()


# Функция для обновления VPN токена и установки срока действия на 30 дней вперёд
async def update_vpn(user_id: int, vpn_token: str):
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    # Установка срока годности VPN на 30 дней вперёд
    vpn_expiration = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("UPDATE users SET vpn_token=?, vpn_expiration=? WHERE id=?", 
                   (vpn_token, vpn_expiration, user_id))
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()

@router.message(F.text == "Профиль")
async def show_profile(message: Message):
    # Подключение к базе данных
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    user_id = message.from_user.id

    # SQL-запрос для получения данных пользователя
    cursor.execute("SELECT name, vpn_token, vpn_expiration FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()  # Получаем данные пользователя

    if user:
        print(f"{Fore.LIGHTYELLOW_EX}Прожали профиль. {Style.RESET_ALL}{datetime.now()}")
        name, vpn_token, vpn_expiration = user

        # Проверка, есть ли подписка и дата окончания
        vpn_token_info = vpn_token if vpn_token else "Отсутсвует"
        vpn_expiration_info = vpn_expiration if vpn_expiration else "Отсутсвует"

        profile_info = (
            f"👤 <b>Ваш профиль</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"📛 <b>Имя:</b> {name}\n"
            f"🔑 <b>VPN Токен:\n</b> <code>{vpn_token_info}</code>\n"
            f"⏳ <b>Срок действия VPN:\n</b> {vpn_expiration_info}\n"
            f"Время бота: {datetime.now()}"
        )
    else:
        profile_info = "Пользователь не найден."
        print(f"{Fore.LIGHTRED_EX}ERR Пользователь запросил профиль, кажется его нету в базе. {Style.RESET_ALL} {datetime.now()}")

    # Ссылка на картинку
    image_url = "https://i.pinimg.com/736x/fe/e6/ea/fee6ea2ac749a0dbcf92027912d40380.jpg"

    # Отправляем картинку с описанием профиля
    await message.answer_photo(photo=image_url, caption=profile_info, parse_mode='HTML', reply_markup=kb.profile)

    # Закрытие соединения с базой данных
    conn.close()

# Обработчик команды "Информация о токене"
@router.message(F.text == "Информация о токене")
async def token_info(message: types.Message):
    # Подключение к базе данных
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    user_id = message.from_user.id

    # SQL-запрос для получения данных о VPN токене и сроке его действия
    cursor.execute("SELECT vpn_token, vpn_expiration FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()  # Получаем данные пользователя

    if user:
        print(f"{Fore.LIGHTYELLOW_EX}Пользователь вывел инфо по подписке. {Style.RESET_ALL}{datetime.now()}")
        vpn_token, vpn_expiration = user

        # Проверка, есть ли токен и срок его действия
        vpn_token_info = vpn_token if vpn_token else "НЕТУ"
        vpn_expiration_info = vpn_expiration if vpn_expiration else "НЕТУ"

        token_message = (
            f"🔑 <b>Информация о вашем VPN токене</b>\n\n"
            f"🔓 <b>Токен:\n</b> <code>{vpn_token_info}</code>\n"
            f"⏳ <b>Срок действия:</b> {vpn_expiration_info}\n\n"
        )

        # Создание инлайн-кнопки для удаления токена
        if vpn_token:  # Если токен есть, предлагается кнопка для его удаления
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Удалить токен", callback_data="delete_token")]
            ])
        else:
            keyboard = None  # Если токена нет, кнопка не показывается

    else:
        token_message = "Пользователь не найден. Прожми /start"
        print(f"{Fore.LIGHTRED_EX}ERR Пользователь запросил инфо о токене, кажется его нету в базе. {Style.RESET_ALL} {datetime.now()}")
        keyboard = None  # Кнопка не показывается, так как пользователя нет

    await message.answer(token_message, parse_mode='HTML', reply_markup=keyboard)

    # Закрытие соединения с базой данных
    conn.close()

# Обработчик инлайн-кнопки для удаления токена
@router.callback_query(F.data == "delete_token")
async def confirm_delete_token(callback_query: CallbackQuery):
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="confirm_delete_token"),
            InlineKeyboardButton(text="Нет", callback_data="cancel_delete_token")
        ]
    ])

    await callback_query.message.edit_text(
        "Вы уверены, что хотите удалить ваш VPN токен?",
        reply_markup=confirm_keyboard
    )

# Обработчик подтверждения удаления токена
@router.callback_query(F.data == "confirm_delete_token")
async def delete_token(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    # Подключение к базе данных
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    # SQL-запрос для удаления VPN токена
    cursor.execute("UPDATE users SET vpn_token=NULL, vpn_expiration=NULL WHERE id=?", (user_id,))
    conn.commit()

    # Логика удаления токена с сервера будет здесь
    # Delete it
    client.delete_key(f"New{user_id} key")
    # -----

    print(f"{Fore.LIGHTYELLOW_EX}Пользователь удалил свой VPN токен. {Style.RESET_ALL}{datetime.now()}")

    await callback_query.message.edit_text(
        "Ваш VPN токен был успешно удален.",
        reply_markup=None
    )

    # Закрытие соединения с базой данных
    conn.close()

# Обработчик отмены удаления токена
@router.callback_query(F.data == "cancel_delete_token")
async def cancel_delete_token(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Удаление VPN токена отменено.",
        reply_markup=None
    )

@router.message(F.text == "Купить впн")
async def show_tariff_plans(message: Message):
    user_id = message.from_user.id  # ID пользователя
    
    # Проверяем активность подписки
    active_subscription_date = check_subscription(user_id)
    
    if active_subscription_date:
        # Если подписка активна, сообщаем об этом пользователю
        await message.answer(f"У вас уже есть активная подписка до {active_subscription_date}.")
        print(f"{Fore.LIGHTYELLOW_EX}Пользователь хотел купить подписку, но она уже имеется. {Style.RESET_ALL}{datetime.now()}")
    else:
        # Если подписка не активна, предлагаем выбрать тарифный план
        await message.answer("Привет! Выбери тарифный план", reply_markup=kb.buy_button)
        print(f"{Fore.LIGHTYELLOW_EX}Нажали кнопку покупки подписки! {Style.RESET_ALL}{datetime.now()}")

# Обработка нажатия на инлайн-кнопку
@router.callback_query(F.data == "buy_vpn_1_month")
async def process_buy_vpn(callback_query: CallbackQuery):
    prices = [LabeledPrice(label="VPN на 1 месяц", amount=15000)]  # 15000 копеек = 150 рублей
    
    await callback_query.message.answer_invoice(
        title="VPN на 1 месяц",
        description="Оплата доступа к VPN на 1 месяц.",
        payload="vpn_1_month",  # Уникальный идентификатор для этого товара
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="vpn-monthly-subscription",
        photo_url="https://hotmart.s3.amazonaws.com/product_pictures/b821dd11-84ab-4b5e-9bfa-a4e7a26608c4/1mo.png",  # Замените на URL картинки
        photo_width=512,
        photo_height=512,
        photo_size=512
    )

# Обработка подтверждения перед оплатой
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    # Отправляем ответ о готовности провести платёж
    await pre_checkout_query.answer(ok=True)

# Обработка успешного платежа
@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    user_id = message.from_user.id
    key = client.create_key(
        key_id=f"New{message.from_user.id} key",
        name=f"BOT-(@{message.from_user.username} ID-({message.from_user.id}) NAME-({message.from_user.full_name}))"
    )

    # Извлечение access_url из объекта vpn_key
    vpn_token = key.access_url
    print(key)
    print(vpn_token)
    
    vpn_expiration = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    key_id=f"New{message.from_user.id} key"

    # Обновление записи пользователя в базе данных
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET vpn_token=?, vpn_expiration=?, key_id=? WHERE id=?", 
                   (vpn_token, vpn_expiration, key_id, user_id))
    conn.commit()
    conn.close()
    print(f"{Fore.GREEN}Пользователь купил подписку! {Style.RESET_ALL}{datetime.now()}")

    # Отправка сообщения с использованием HTML
    await message.answer(
        f"Спасибо за покупку! \nВаш VPN активен до {vpn_expiration}.\nВаш токен:\n<code>{vpn_token}</code>",
        parse_mode='HTML'
    )

@router.message(F.text == "Назад")
async def exitt(message: Message):
  await message.answer('Вы вернулись на главную.', reply_markup=kb.main)

@router.message(F.text == "Поддержка")
async def exitt(message: Message):
    await message.answer("Привет\nПо вопросам писать в бота.\nБот: \n||Он не отвечает. Увижу, отвечу.||")
    print(f"{Fore.LIGHTYELLOW_EX}Нажали на поддержку. {Style.RESET_ALL}{datetime.now()}")
