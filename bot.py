import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from env_config import TOKEN

from functions import *


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    '''
    Хендлер команды "/start"
    '''
    await message.answer('Hello!')


@dp.message()
async def main_func(message: types.Message) -> None:
    '''
    Основная функция
    '''
    try:
        message_dict = json.loads(message.text)
        collection = collection_find(database.sample_collection, message_dict)
        r = agregation(collection, message_dict['group_type'])
        result = json.dumps(r)
    except:
        result = 'Ошибка формата ввода'

    finally:
        await bot.send_message(message.chat.id, result)


async def main() -> None:
    '''
    Поллинг объектов
    '''
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

