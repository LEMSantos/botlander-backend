from mongoengine import Document
from mongoengine import (
    StringField,
    EmailField,
)


class User(Document):

    meta = {
        'collection': 'users'
    }

    name = StringField(max_length=100, required=True)
    lastname = StringField(max_length=100, required=True)
    username = StringField(max_length=100, required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
