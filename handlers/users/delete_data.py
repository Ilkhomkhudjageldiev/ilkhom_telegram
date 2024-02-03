from loader import dp, db
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from states.register_state import Register


@dp.callback_query_handler(text=['add', 'edit', 'delete'])
async def update_data(call: CallbackQuery, state: FSMContext):
    if call.data == 'delete':
        # await call.answer()
        await call.message.answer('product_name')

