import asyncio
from aiogram.utils import executor
from Bot.dispatcher import dp

if __name__ == '__main__':
    import os
    import sys

    # Устанавливаем рабочую директорию в корень проекта
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        executor.start_polling(dp, skip_updates=True)
    except KeyboardInterrupt:
        pass
