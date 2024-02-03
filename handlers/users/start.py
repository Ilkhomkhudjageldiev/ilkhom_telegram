from aiogram.dispatcher.filters.builtin import CommandStart, Message, CallbackQuery
from keyboards.inline.inline_menu import *
from loader import dp, db

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


@dp.callback_query_handler(text=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
async def order(call: CallbackQuery):
    btn = await product()
    call_data = call.data
    data = await db.get_product_info(call_data)
    for item in data:
        path = item['product_photo']
    # await call.message.answer(item['product_name'])
    # await call.message.answer_photo(path)
    # await call.message.answer(f"""{item['product_name']}. Narxi: {item['product_price']}""", reply_markup=btn)

    await call.message.answer(f"""
{item['product_name']}

{await call.message.answer_photo(path)}

Narxi: {item['product_price']}""", reply_markup=btn)


