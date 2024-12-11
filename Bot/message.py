from aiogram.types import InputFile, InputMediaPhoto

from .bot import bot
from .keyboard import *
from DataBase.models import FormData
from utils.get_config import load_config


async def send_start_message(chat_id):
    text = """
Здравствуйте ! Добро пожаловать в Velvet Glamour

У нас вы можете найти лучших девочек для интимных встреч.

Выдача адресов происходит круглосуточно через бота или, в крайних случаях, через куратора!

Внимательней проверяйте адрес Telegram, остерегайтесь мошенников, спасибо, что выбираете нас!
    """
    photo = InputFile("src/images/1.jpg")

    await bot.send_photo(chat_id, photo, caption=text, reply_markup=create_main_keyboard())


async def send_post_model(data: dict) -> str:
    config = load_config()
    channel_id = config["bot"]["channel"]
    text = f"""
😍 {data["name"]} • {data["age"]}

🌇 Час - {data["price_1h"]}₽
🏙 2 часа - {data["price_2h"]}₽
🌃 Ночь - {data["price_night"]}₽

Рост: {data["height"]}, грудь: {data["bosom"]}.
        """
    photos = list(map(lambda photo: InputMediaPhoto(media=photo), data["photos"]))
    photos[0].caption = text
    message = await bot.send_media_group(chat_id=channel_id, media=photos)
    return message[0].url


async def send_model_info(chat_id: int, model_id: int, current_index: int = 0):
    model = FormData.get(id=model_id)

    text = f"""
😍 {model.name} • {model.age}

🌇 Час - {model.price_1h}₽
🏙 2 часа - {model.price_2h}₽
🌃 Ночь - {model.price_night}₽

Рост: {model.height}, грудь: {model.bosom}.

ℹ️ Для оформления нажмите на кнопку Оформить
    """

    # Разбиваем фотографии на список
    photos = model.photos.split(",")
    photo_id = photos[current_index]

    await bot.send_photo(chat_id, photo=photo_id, caption=text,
                         reply_markup=create_model_info_keyboard(model_id, current_index))


async def send_reservation_info(chat_id):
    text = """
Уточните пожалуйста следующие детали брони :
- Дата и время встречи;
- Место встречи (адрес, где состоится встреча, у Вас или у модели);
- Контактные данные для связи с вами (Ваш номер телефона или Telegram)
    """
    await bot.send_message(chat_id, text, reply_markup=cancel_keyboard())
