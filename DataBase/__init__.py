from .models import FormData
from .database import db

db.connect()
db.create_tables([FormData])
