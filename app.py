from aiogram import executor

import logging

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands, set_default_commands_guest
from data.config import ADMINS

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)


    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    # Database ishlatish
    await db.conf()

    # User jadvali yoq bolsa yaratish
    await db.create_table_users()
    await db.create_table_day_types()
    await db.create_table_product()
    await db.create_table_order_item()

    car_list = [('car', '🚗 Yengil mashina'), ('gazel', '🛻 Gazel'),('isuzu', '🚛 Isuzu')]
    week = [('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'),
            ('friday', 'Friday')]

    # await db.insert_day_types(week)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
