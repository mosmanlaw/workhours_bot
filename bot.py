import asyncio
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,   # выводим DEBUG для максимально подробной информации
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

print("=== Bot is starting (DEBUG logging enabled) ===")

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from app.settings import settings
from app.handlers import common, worked, paid, cash, registration

async def main():
    # Инициализация Bot с указанием DefaultBotProperties для parse_mode
    bot = Bot(
        settings.bot_token,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    # Диспетчер обновлений
    dp = Dispatcher()
    # Регистрируем все роутеры из модулей-обработчиков
    dp.include_routers(
        common.router,
        worked.router,
        paid.router,
        cash.router,
        registration.router,
    )
    # Запускаем поллинг
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
