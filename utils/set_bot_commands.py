from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(

        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("update", "Ma'lumotni o'zgartirish"),
            types.BotCommand("help", "Yordam"),
        ]
    )


async def set_default_commands_guest(dp):
    await dp.bot.set_my_commands(

        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
        ]
    )