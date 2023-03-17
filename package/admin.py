#-*- coding: utf-8 -*-
from vars import dp, bot
from aiogram import types, Dispatcher
from database import db
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import random
import os


async def info(message: types.Message):
    await bot.send_message(message.from_user.id, "*Команды администратора*:\n\nДобавить пользователя: /add\nОтменить добавление полльзователя: /cancel\nУдалить пользователя: /del\nСписок всех пользователей: /all")


class FSM_add_user(StatesGroup):
    password = State()
    user_link = State()
    access_key = State()
    

async def add_user_start_fsm(message: types.Message):
    await FSM_add_user.password.set()
    await bot.send_message(message.from_user.id, "Чтобы добавить пользователя введите *ПАРОЛЬ*")


async def cancel_fsm(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state == None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, "Добавление пользователя отменено")


async def check_password_fsm(message: types.Message, state: FSMContext):
    if message.from_user.id == 585954737 or message.from_user.id == 1468286116 or message.from_user.id == 1117594782 or message.text == "t9Ll":
        await FSM_add_user.next()
        await bot.send_message(message.from_user.id, 'Введите *ССЫЛКУ* на пользователя без знака "@"')
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "Неверный пароль")
        
        
async def add_user_fsm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["user_link"] = message.text
        data["ID"] = ""
    await FSM_add_user.next()
    await bot.send_message(message.from_user.id, "Чтобы подтвердить действие, введите любое слово")
    
    
async def generate_access_key_fsm(message: types.Message, state: FSMContext):
    
    alph = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ln = len(alph)-1
    access_key = ""
    
    for _ in range(20):
        access_key += alph[random.randint(0, ln)]
    
    async with state.proxy() as data:
        data["access_key"] = access_key
        await db.add_user(data)

    await state.finish()
    await bot.send_message(message.from_user.id, f" Пользователь добавлен:\nUser: *@{tuple(data.values())[0]}*\nКод доступа: `{access_key}`")






class FSM_del_user(StatesGroup):
    password = State()
    user_id = State()
    

async def del_user_start_fsm(message: types.Message):
    await FSM_del_user.password.set()
    await bot.send_message(message.from_user.id, "Чтобы удалить пользователя введите *ПАРОЛЬ*")


async def check_password_fsm2(message: types.Message, state: FSMContext):
    if message.text == "123":
        await FSM_del_user.next()
        await bot.send_message(message.from_user.id, "Введите *ID* пользователя")
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "Неверный пароль")
        
        
async def del_user_id_fsm(message: types.Message, state: FSMContext):
    await db.dell_user(message.text)
    await state.finish()
    
    
async def all_users(message:types.Message):
    if message.from_user.id == 585954737 or message.from_user.id == 1468286116 or message.from_user.id == 1117594782:
        data = db.all_users()
        print(data)
        users = ""
        for i in data:
            users += "@" + i[0] + "\n"
        await bot.send_message(message.from_user.id, "Список всех пользователей:\n\n" + users)
    else:
        await bot.send_message(message.from_user.id, "У вас нет права доступа к этой команде")


def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(info, commands=["commands"])
    dp.register_message_handler(add_user_start_fsm, commands=["add"])
    dp.register_message_handler(cancel_fsm, commands=["cancel"], state="*")
    dp.register_message_handler(check_password_fsm, state=FSM_add_user.password)
    dp.register_message_handler(add_user_fsm, state=FSM_add_user.user_link)
    dp.register_message_handler(generate_access_key_fsm, state=FSM_add_user.access_key)
    dp.register_message_handler(del_user_start_fsm, commands=["del"])
    dp.register_message_handler(check_password_fsm2, state=FSM_del_user.password)
    dp.register_message_handler(del_user_id_fsm, state=FSM_del_user.user_id)
    dp.register_message_handler(all_users, commands=["all"])