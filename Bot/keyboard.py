from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from DataBase.models import FormData


def create_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row(KeyboardButton("💖 Модели"))
    keyboard.row(
        KeyboardButton("👤 Профиль"),
        KeyboardButton("🔍 Информация")
    )
    keyboard.row(
        KeyboardButton("✍ Подать анкету"),
        KeyboardButton("👨‍💻 Техническая поддержка")
    )
    return keyboard


def cancel_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("❌ Отмена"))
    return keyboard


pagination_cb = CallbackData('paginator', 'page')
model_cb = CallbackData('model', 'model_id')


def get_pagination_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    forms = FormData.select()
    keyboard = InlineKeyboardMarkup(row_width=3)

    for form in forms[(current_page - 1) * 4:(current_page - 1) * 4 + 4]:
        keyboard.add(InlineKeyboardButton(f"{form.name}, {form.age}", callback_data=model_cb.new(model_id=form.id)))

    if current_page > 1:
        keyboard.add(InlineKeyboardButton(
            "⬅️ Назад",
            callback_data=pagination_cb.new(page=current_page - 1)
        ))
        keyboard.insert(InlineKeyboardButton(
            f"{current_page}/{total_pages}",
            callback_data="current_page"
        ))

    else:
        keyboard.add(InlineKeyboardButton(
            f"{current_page}/{total_pages}",
            callback_data="current_page"
        ))

    if current_page < total_pages:
        keyboard.insert(InlineKeyboardButton(
            "Вперед ➡️",
            callback_data=pagination_cb.new(page=current_page + 1)
        ))

    return keyboard


photo_cb = CallbackData("photo", "id", "current_index")
reservation_cb = CallbackData("reservation", "model_id")


def create_model_info_keyboard(model_id: int, current_index: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            "Другое фото",
            callback_data=photo_cb.new(id=model_id, current_index=current_index),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            "Забронировать",
            callback_data=reservation_cb.new(model_id=model_id),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            "⏪ Назад",
            callback_data=pagination_cb.new(page=1),
        )
    )

    return keyboard
