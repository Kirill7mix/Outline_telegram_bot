import asyncio
import logging
from conf import TOKEN, api_url, cert_sha256, PAYMENTS_PROVIDER_TOKEN
from app.router import router
from aiogram import Bot, Dispatcher
import sqlite3
from datetime import datetime
from colorama import Fore, Back, Style, init
from outline_vpn.outline_vpn import OutlineVPN
from random import randint

bot = Bot(token=TOKEN)
dp = Dispatcher()

#Доп. Для проверки подписки.
async def delete_expired_keys():
    client = OutlineVPN(api_url=api_url, cert_sha256=cert_sha256)

    while True:
        await asyncio.sleep(5)
        print(f"{Fore.LIGHTBLACK_EX}Обновление учатсников..... {Style.RESET_ALL}{datetime.now()}")
        conn = sqlite3.connect('bot_users.db')
        cursor = conn.cursor()

        # СЕЙЧАС.
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Детектим должников
        cursor.execute("SELECT id, key_id FROM users WHERE vpn_expiration < ?", (now,))
        expired_users = cursor.fetchall()

        for user_id, key_id in expired_users:
            if key_id:  # Проверка
                # Удаляем ключ из Outline VPN Manager
                try:
                    status_delete_key = client.delete_key(key_id)
                    print(status_delete_key)
                    print(f"{Fore.LIGHTBLACK_EX}Удалён ключ {key_id} для пользователя {user_id}. {Style.RESET_ALL}{datetime.now()}")
                except Exception as e:
                    print(f"{Fore.LIGHTRED_EX}Ошибка при удалении ключа {key_id}: {e} {Style.RESET_ALL}{datetime.now()}")

            # Удаляем VPN токен из базы
            cursor.execute("UPDATE users SET vpn_token=NULL, vpn_expiration=NULL WHERE id=?", (user_id,))
            print(f"VPN-токен для пользователя {user_id} удалён из базы данных. {datetime.now()}")

        # Сохраняем, закрываем
        conn.commit()
        conn.close()

        # Тут типо ждём 1 час gthtl cktle.otq ghjdthrjq
        print(f"{Fore.LIGHTBLACK_EX}ОКЕ! {Style.RESET_ALL}{datetime.now()}")
        await asyncio.sleep(3600)

async def main():
    dp.include_router(router)
    
    # Запуск До проверки подписки.
    asyncio.create_task(delete_expired_keys())
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'Bot stopped {datetime.now()}')

#Иной код