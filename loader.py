from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode

from config import TOKEN
from utils.db_api.db import Database

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# db = Database(db_name=DB_NAME,
#               db_user=DB_USER,
#               db_password=DB_PASSWORD,
#               db_host=DB_HOST,
#               db_port=DB_PORT)

