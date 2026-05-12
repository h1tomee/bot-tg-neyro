import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.core.config import settings
from bot.handlers import common

async def main():
    # Настройка логирования: INFO позволит видеть в консоли, кто пишет боту и какие есть ошибки
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("BotErrors.log"),
            logging.StreamHandler()
        ]
    )
    
    # Инициализируем бота, забирая токен из нашего конфига
    bot = Bot(token=settings.bot_token.get_secret_value())
    
    # Диспетчер — это главный распределитель. Он получает сообщение и смотрит, какой роутер его обработает
    dp = Dispatcher()

    # Подключаем наш роутер из шага 2
    dp.include_router(common.router)

    print("Бот запущен!")
    
    # start_polling — бот начинает постоянно спрашивать сервер Telegram: "Мне кто-нибудь написал?"
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запуск асинхронного цикла
    asyncio.run(main())