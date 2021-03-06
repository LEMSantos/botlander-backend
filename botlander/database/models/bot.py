from mongoengine import Document
from mongoengine import (
    StringField,
    ImageField,
    ReferenceField,
)
from mongoengine import CASCADE
from botlander.database.models import User
import uuid


class Bot(Document):

    meta = {
        'collection': 'bots'
    }

    name = StringField(
        max_length=100,
        required=True,
        unique=True
    )
    description = StringField(max_length=300)
    image = ImageField()
    api_token = StringField(default=lambda: str(uuid.uuid4()), unique=True)
    telegram_token = StringField()
    user_id = ReferenceField(
        User,
        required=True,
        reverse_delete_rule=CASCADE
    )
