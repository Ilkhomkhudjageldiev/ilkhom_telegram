from aiogram.contrib.middlewares import logging
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp, db, bot
from aiogram.types import CallbackQuery, Message
from keyboards.inline.inline_menu import *
from states.register_state import Register


@dp.callback_query_handler(text=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
async def order(call: CallbackQuery):
    call_data = call.data
    await call.answer()
    day_id = await db.get_day_id(call_data)
    data = await db.get_product_info(call_data)
    btn = await product(day_id=day_id)
    item=''
    for item in data:
        path = item['product_photo']
    text = f"""{item['product_name']}. Narxi:{item['product_price']}"""
    await call.message.answer_photo(photo=path, caption=text, reply_markup=btn)


@dp.callback_query_handler(text=['plus', 'minus'])
async def calc(call: CallbackQuery):
    if call.data == 'plus':
        quantity = int(call.message.reply_markup.inline_keyboard[0][1].text)
        day_id = call.message.reply_markup.inline_keyboard[1][0].callback_data

        if quantity < 10:
            quantity += 1
            btn = await product(day_id=day_id, quantity=quantity)
            await call.message.edit_reply_markup(reply_markup=btn)

        else:
            await call.answer(text='Maxsimum qiymatga yetib keldi❗', show_alert=True)

    elif call.data == 'minus':
        quantity = int(call.message.reply_markup.inline_keyboard[0][1].text)
        day_id = call.message.reply_markup.inline_keyboard[1][0].callback_data
        if quantity > 1:
            quantity -= 1
            btn = await product(day_id=day_id, quantity=quantity)
            await call.message.edit_reply_markup(reply_markup=btn)
        else:
            await call.answer(text='Minimum qiymatga yetib keldi❗', show_alert=True)


@dp.callback_query_handler(text=[i for i in range(1,8)])
async def order(call: CallbackQuery, state: FSMContext):
    btn = await payment_types_btn()
    day_id = call.data
    quantity = int(call.message.reply_markup.inline_keyboard[0][1].text)
    data = await db.get_product_order(int(day_id))
    for item in data:
        item
    product_price = item['product_price']
    product_name = item['product_name']
    product_total_price = quantity*int(product_price)
    await call.message.answer('Comments:')
    await Register.comments.set()

    @dp.message_handler(state=Register.comments)
    async def comments(msg: Message, state: FSMContext):
        # await msg.delete()
        comment = msg.text
        # comment = call.message.text
        await state.update_data({'comment': comment})
        await call.message.answer("Ismingiz va hona raqami kiriting:")
        await Register.name_room.set()

    @dp.message_handler(state=Register.name_room)
    async def name_room(msg: Message, state: FSMContext):
        name_room = msg.text
        # name_room = call.message.text
        await state.update_data({'name_room': name_room})
        data = await state.get_data()
        await state.finish()
        for i in data:
            print(i)
        await call.message.answer(f"""To'lov turini tanlang:""", reply_markup=btn)

        @dp.callback_query_handler(text=['cash', 'transfer'])
        async def payment(call: CallbackQuery):
            payment_type = call.data
            if call.data == 'cash':
                await call.message.answer(f"""Total: {product_total_price}sum
Comments: {data['comment']}
Name_room: {data['name_room']}
Naqd""")

            elif call.data == 'transfer':
                await call.message.answer(f"""Total: {product_total_price}sum
Comments: {data['comment']}
Name_room: {data['name_room']}
Carta raqami: xxxx-xxxx-xxxx-xxxx""")
            day_type = await db.get_day_type(day_id)
            await db.insert_customer_info_order(day_type, call.from_user.username, payment_type, product_name, quantity, product_price, product_total_price, f"""{data['comment']} {data['name_room']}""")
            for admin in ADMINS:
                try:
                    await bot.send_message(admin, "done")

                except Exception as err:
                    logging.exception(err)