from mongoengine import (
    Document,
    ReferenceField,
    IntField,
    BooleanField,
    StringField,
)

class Paymant(Document):
    price = IntField(required = True)
    name = StringField()
