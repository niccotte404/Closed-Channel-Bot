#-*- coding: utf-8 -*-
from vars import dp, bot
from aiogram.utils import executor
from package import admin, user
from database import db

async def on_startup(_):
    print("Bot started OK")
    db.create_db()
    
admin.reg_handlers(dp)
user.reg_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)