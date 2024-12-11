from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    age = State()
    height = State()
    bosom = State()
    price_1h = State()
    price_2h = State()
    price_night = State()
    photos = State()


class Reservation(StatesGroup):
    text = State()
