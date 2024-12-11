from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .Middlewares.AlbumMiddleware import AlbumMiddleware
from utils.get_config import load_config
from .Filters.IsUserInGroup import IsUserInGroup

# Загружаем конфигурацию
config = load_config()

bot = Bot(config["bot"]["token"], parse_mode="HTML")
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(AlbumMiddleware())
dp.filters_factory.bind(IsUserInGroup)