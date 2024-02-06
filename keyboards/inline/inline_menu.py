from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



async def start_button():
    menu = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Buyurtmachi', callback_data='customer'),
        InlineKeyboardButton(text='Haydovchi', callback_data='driver')
    ]])
    return menu


async def order_button():
    menu = InlineKeyboardMarkup()
    menu.insert(InlineKeyboardButton(text='Buyurtma berish', callback_data='order'))
    return menu


async def car_menu(car_list):
    menu = InlineKeyboardMarkup(row_width=1)
    for inner in car_list:
        menu.insert(InlineKeyboardButton(text=inner[1], callback_data=inner[0]))
    return menu




async def payment_btn():
    menu = InlineKeyboardMarkup(row_width=1)
    menu.insert(InlineKeyboardButton(text='Yuboruvchi', callback_data='sender'))
    menu.insert(InlineKeyboardButton(text='Qabul qiluvchi', callback_data='receiver'))
    return menu


async def ok_skip_btn():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='OK', callback_data='ok'),
         InlineKeyboardButton(text="O'tkazib yuborish", callback_data='skip')]])
    return menu


async def button(callback=None):
    menu = InlineKeyboardMarkup()
    menu.insert(InlineKeyboardButton(text=callback, callback_data=callback))
    return menu


async def common_btn(data_list):
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=item[1], callback_data=item[0]) for item in data_list]
    ])
    return menu


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
async def menu_button():
    menu = InlineKeyboardMarkup()
    menu.insert(InlineKeyboardButton(text='Menu🍽️🥩🥗', callback_data='menu'))
    return menu


async def week_button(data_list):
    menu = InlineKeyboardMarkup(row_width=3)
    for item in data_list:
        menu.insert(InlineKeyboardButton(text=item[1], callback_data=item[0]))
    return menu

async def admin_btn():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='add', callback_data='add'),
         InlineKeyboardButton(text='edit', callback_data='edit'),
         InlineKeyboardButton(text="delete", callback_data='delete')]])
    return menu


async def product(day_id=None, quantity=None):
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='➖', callback_data='minus'),
            InlineKeyboardButton(text='1' if not quantity else quantity, callback_data='quantity'),
            InlineKeyboardButton(text='➕', callback_data='plus')
        ],
        [
            InlineKeyboardButton(text='order', callback_data=day_id)
        ]

    ])
    return menu


async def payment_types_btn():
    menu = InlineKeyboardMarkup(row_width=1)
    menu.insert(InlineKeyboardButton(text='Naqd🫰', callback_data='cash'))
    menu.insert(InlineKeyboardButton(text="Pul o'tkazish💵", callback_data='transfer'))
    return menu

