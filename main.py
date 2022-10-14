import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from parser import ParsePublic

from database import Base, engine

token = os.getenv('TG_TOKEN')

catButton = KeyboardButton('/cats')
memeButton = KeyboardButton('/memes')
client_buttons = ReplyKeyboardMarkup()
client_buttons.add(catButton).add(memeButton)

bot = Bot(token=token)
dispatcher = Dispatcher(bot=bot)


@dispatcher.message_handler(commands=['cats'])

async def Stuff(message: types.Message):
    """ассинхронно парсит паблики с котами"""
    urls = ParsePublic(message.from_user.id,
                       ['kotany_university', 'mya_bl', 'kotikihujotiki', 'obscene_cat', 'ilovekitsi', 'vetsovet'],
                       'cats')
    for url in urls:
        await bot.send_photo(photo=url, chat_id=message.chat.id)


@dispatcher.message_handler(commands=['memes'])
async def Stuff(message: types.Message):
    """ассинхронно парсит паблики с мемами"""
    urls = ParsePublic(message.from_user.id,
                       ['saintbeobanka', 'cursed_hh'], 'memes')
    for url in urls:
        await bot.send_photo(photo=url, chat_id=message.chat.id)


async def InitFunc(_):
    Base.metadata.create_all(engine)


executor.start_polling(dispatcher=dispatcher, skip_updates=True, on_startup=InitFunc)
