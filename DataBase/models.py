from peewee import Model, TextField, IntegerField
from .database import db


class FormData(Model):
    name = TextField()
    age = IntegerField()
    height = TextField()
    bosom = TextField()
    price_1h = IntegerField()
    price_2h = IntegerField()
    price_night = IntegerField()
    photos = TextField()  # Храним фото как строку через запятую
    url = TextField(default="")

    class Meta:
        database = db  # Используем базу данных db
