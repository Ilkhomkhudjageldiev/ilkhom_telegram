from aiogram.dispatcher.filters.builtin import CommandStart, Message, CallbackQuery
from keyboards.inline.inline_menu import *
from loader import dp, db, bot


week = [('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday')]


@dp.message_handler(CommandStart())
async def bot_start(msg: Message):
    menu = await menu_button()
    await msg.answer(f"Assalomu aleykum,\nLogistika markaziga xush kelibsiz!", reply_markup=menu)


@dp.callback_query_handler(text='menu')
async def menu_btn(call: CallbackQuery):
    await call.answer()
    btn = await week_button(week)
    await call.message.answer(f"Hurmatli mijoz, Hafta kunini tanlang: ", reply_markup=btn)





