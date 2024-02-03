from aiogram.dispatcher.filters.state import State, StatesGroup

class Register(StatesGroup):
    full_name = State()
    phone_number = State()
    product_name = State()
    product_photo = State()
    product_price = State()
    subcategory_id = State()
    destination = State()
    receiver_phone_number = State()
    load_time = State()
    comments = State()
