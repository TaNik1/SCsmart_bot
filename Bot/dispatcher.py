from aiogram import types
from aiogram.dispatcher import filters
from aiogram.utils.exceptions import BadRequest
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

from .bot import dp
from .message import *
from .States import *
from DataBase.models import *


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    await send_start_message(user_id)


@dp.message_handler(commands=['create_form'], is_admin=True)
async def start_form(message: types.Message):
    await message.answer("Введите имя:", reply_markup=cancel_keyboard())
    await Form.name.set()


@dp.message_handler(filters.Text(equals="❌ Отмена"), state="*")
async def cancel_any_state(message: types.Message, state: FSMContext):
    await state.finish()
    await send_start_message(message.from_user.id)


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите возраст:", reply_markup=cancel_keyboard())
    await Form.next()


@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return

    await state.update_data(age=int(message.text))
    await message.answer("Введите рост:", reply_markup=cancel_keyboard())
    await Form.next()


@dp.message_handler(state=Form.height)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.answer("Введите размер груди:", reply_markup=cancel_keyboard())
    await Form.next()


@dp.message_handler(state=Form.bosom)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(bosom=message.text)
    await message.answer("Введите ценник на 1 час:", reply_markup=cancel_keyboard())
    await Form.next()


@dp.message_handler(state=Form.price_1h)
async def process_price_1h(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return

    await state.update_data(price_1h=message.text)
    await message.answer("Введите ценник на 2 часа:", reply_markup=cancel_keyboard())
    await Form.next()


@dp.message_handler(state=Form.price_2h)
async def process_price_2h(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return

    await state.update_data(price_2h=message.text)
    await message.answer("Введите ценник на всю ночь:", reply_markup=cancel_keyboard())
    await Form.next()


@dp.message_handler(state=Form.price_night)
async def process__price_night(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return

    await state.update_data(price_night=message.text)
    await message.answer("Загрузите фотографии (можете отправить несколько):", reply_markup=cancel_keyboard())
    await Form.next()


@dp.message_handler(content_types=['photo'], state=Form.photos)
async def process_photos(message: types.Message, state: FSMContext, album: List[types.Message] = None):
    photos = []
    try:
        for msg in album:
            photos.append(msg.photo[-1].file_id)
    except TypeError:
        photos.append(message.photo[-1].file_id)

    await state.update_data(photos=photos)

    data = await state.get_data()
    url = await send_post_model(data)
    FormData.create(
        name=data['name'],
        age=data['age'],
        height=data['height'],
        bosom=data["bosom"],
        price_1h=data['price_1h'],
        price_2h=data['price_2h'],
        price_night=data['price_night'],
        photos=",".join(data['photos']),
        url=url)

    await message.answer("Данные сохранены успешно!")
    await state.finish()
    await send_start_message(message.from_user.id)


@dp.message_handler(filters.Text(equals="💖 Модели"))
async def all_models(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"💝 Все анкеты проходили строгую проверку личности нашим агентством. Свободны сейчас: "
                           f"{len(FormData.select())}",
                           reply_markup=get_pagination_keyboard(1, (len(FormData.select()) - 1) // 4 + 1))


@dp.callback_query_handler(pagination_cb.filter())
async def handle_pagination_callback(call: types.CallbackQuery, callback_data: dict):
    current_page = int(callback_data['page'])
    total_pages = (len(FormData.select()) - 1) // 4 + 1

    try:
        await call.message.edit_reply_markup(
            reply_markup=get_pagination_keyboard(current_page, total_pages)
        )
    except BadRequest:
        await bot.send_message(call.from_user.id,
                               f"💝 Все анкеты проходили строгую проверку личности нашим агентством. Свободны сейчас: "
                               f"{len(FormData.select())}",
                               reply_markup=get_pagination_keyboard(current_page, total_pages))
    await call.answer()


@dp.callback_query_handler(model_cb.filter())
async def process_model(call: types.CallbackQuery, callback_data: dict):
    await send_model_info(call.from_user.id, int(callback_data["model_id"]))


@dp.callback_query_handler(photo_cb.filter())
async def switch_photo(call: types.CallbackQuery, callback_data: dict):
    model_id = int(callback_data["id"])
    current_index = int(callback_data["current_index"])

    model = FormData.get(id=model_id)

    photos = model.photos.split(",")
    new_index = (current_index + 1) % len(photos)

    await bot.edit_message_media(
        media=types.InputMediaPhoto(media=photos[new_index], caption=call.message.caption),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=create_model_info_keyboard(model_id, new_index),
    )


@dp.callback_query_handler(reservation_cb.filter())
async def reservation_process(call: types.CallbackQuery, callback_data: dict):
    await send_reservation_info(call.from_user.id)
    await Reservation.text.set()
    await dp.current_state().update_data(model_id=callback_data["model_id"])


@dp.message_handler(state=Reservation.text)
async def reservation_accept(message: types.Message, state: FSMContext):
    config = load_config()
    admin_chat = config["bot"]["admin_chat"]
    data = await state.get_data()
    model_id = data["model_id"]
    model = FormData.get(id=model_id)

    await bot.send_message(admin_chat, message.text + f"\n\nМодель: {model.url}")
    await message.answer("Бронь оставлена!")
    await send_start_message(message.from_user.id)
    await state.finish()