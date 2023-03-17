from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

bot = Bot(token="", parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=MemoryStorage())