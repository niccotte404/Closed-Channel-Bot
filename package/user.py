#-*- coding: utf-8 -*-
from os import access
from vars import dp, bot
from aiogram import types, Dispatcher
from database import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class FSMauth(StatesGroup):
    db = State()
    auth = State()


async def fsm_start(message: types.Message, state=FSMContext):
    
    await FSMauth.db.set()
    username = message.from_user.username
    user_id = message.from_user.id
    print(db.check_user(username), db.check_id(user_id))
    print(username, user_id)

    if db.check_user(username) or db.check_id(user_id):
        await bot.send_message(message.from_user.id, "Введите *ключ доступа*:")
        await db.add_user_id(username, user_id)
        await FSMauth.next()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "Вы не зарегестрированы на платформе\n\n*Для повторной авторизации введите команду /auth*\n\nЕсли произршла ошибка, обратитесь в службу поддержки: @elizabeethz")


async def urls(message: types.Message, state: FSMContext):
    
    username = message.from_user.username
    user_id = message.from_user.id
    access_key = db.select_access_key(user_id)
    print(username, user_id)
    
    if message.text == access_key or user_id == 1468286116 or user_id == 1117594782 or user_id == 585954737:
        
        ikm = InlineKeyboardMarkup(row_width=3)
        reviewBtn = InlineKeyboardButton(text="Отзывы", url="https://t.me/+BI8Uc_632dEwM2Qy")
        fichaBtn = InlineKeyboardButton(text="Фишки", url="https://t.me/+BJbInOrtiBw3YWJi")
        articlesBtn = InlineKeyboardButton(text="Обучение", url="https://t.me/+N0u4c59mmD0wYTIy")
        baseBtn = InlineKeyboardButton(text="Основной канал", url="https://t.me/+1lbe5MdC5mc3MmQy")
        ikm.add(articlesBtn, fichaBtn, reviewBtn)
        ikm.add(baseBtn)
        
        await bot.send_photo(message.from_user.id, "AgACAgIAAxkBAAPUYxe14pQtUHvn0Uj8n7jIFzREsjMAAqG8MRune8BIGWj3TSIVuxABAAMCAAN5AAMpBA", reply_markup=ikm)
        await state.finish()
        
    else:
        await bot.send_message(message.from_user.id, "*Неверный* ключ доступа")
        await state.finish()
        await fsm_start(message, state)


# async def pic(message: types.Message):
#     print(message.photo[-1].file_id)


def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=["start", "auth"])
    dp.register_message_handler(urls, state=FSMauth.auth)
    # dp.register_message_handler(pic, content_types=["photo"])