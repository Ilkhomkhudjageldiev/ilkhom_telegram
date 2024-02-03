from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Message, CallbackQuery
from keyboards.inline.inline_menu import *
from loader import dp, db
from states.register_state import Register


@dp.message_handler(commands=['update', ])
async def admin(msg: Message):
    menu = await admin_btn()
    await msg.answer(f"ADMIN panelga xush kelibsiz!", reply_markup=menu)


@dp.callback_query_handler(text=['add', 'edit', 'delete'])
async def update_data(call: CallbackQuery, state: FSMContext):
    if call.data == 'add':
        # await call.answer()
        await call.message.answer('product_name')
        await Register.product_name.set()

    @dp.message_handler(state=Register.product_name)
    async def get_product_name(msg: Message, state: FSMContext):
        # await msg.answer()
        product_name = msg.text
        await state.update_data({'product_name': product_name})
        await msg.answer('product_photo')
        await Register.product_photo.set()

    @dp.message_handler(lambda msg: not msg.photo, state=Register.product_photo)
    async def get_product_photo_check(msg: Message):
        await msg.answer('product_photo')
        await Register.product_photo.set()

    @dp.message_handler(state=Register.product_photo, content_types='photo')
    async def get_product_photo(msg: Message, state: FSMContext):
        product_photo = msg.photo[0].file_id
        await state.update_data({'product_photo': product_photo})
        await msg.answer('product_price')
        await Register.product_price.set()

    @dp.message_handler(state=Register.product_price)
    async def get_product_price(msg: Message, state: FSMContext):
        product_price = msg.text
        if product_price.isdigit():
            await state.update_data({'product_price': product_price})
            await msg.answer('subcategory_id')
            await Register.subcategory_id.set()
        else:
            await msg.answer('product_price')
            await Register.product_price.set()

    @dp.message_handler(state=Register.subcategory_id)
    async def get_subcategory_id(msg: Message, state: FSMContext):
        subcategory_id = msg.text
        if subcategory_id.isdigit():
            await state.update_data({'subcategory_id': int(subcategory_id)})
            data = await state.get_data()
            await state.finish()
            await db.insert_product_data(data['product_name'], data['product_photo'], data['product_price'], data['subcategory_id'])
        else:
            await msg.answer('subcategory_id')
            await Register.subcategory_id.set()