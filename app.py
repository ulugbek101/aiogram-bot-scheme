import asyncio
import logging

from loader import dp, bot
from handlers.start import router


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(router=router)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
