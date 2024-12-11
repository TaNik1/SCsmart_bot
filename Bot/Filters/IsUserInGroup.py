from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.get_config import load_config

config = load_config()


class IsUserInGroup(BoundFilter):
    key = 'is_admin'  # Имя фильтра

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: types.Message) -> bool:
        try:
            chat_member = await message.bot.get_chat_member(config["bot"]["admin_chat"], message.from_user.id)
            # Если is_user_in_group == True, проверяем, что пользователь состоит в группе
            # Если is_user_in_group == False, проверяем, что пользователь не состоит в группе
            return chat_member.status in ['member', 'administrator',
                                          'creator'] if self.is_admin else chat_member.status == 'left'
        except Exception as e:
            # В случае ошибки (например, если бот не администратор), можно вернуть False
            print(f"Ошибка при проверке состояния пользователя: {e}")
            return False
