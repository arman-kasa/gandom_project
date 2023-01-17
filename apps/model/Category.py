from mongoengine import Document, IntField, StringField, ReferenceField
from flask import request
from apps.model.user import User
from apps.utils import get_user_by_token

class Category(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)
    user = ReferenceField(User, required=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def populate(self, json):
        self.id = json["id"]
        self.name = json["name"]
        self.user = User.objects.get(
            username=get_user_by_token(request.headers["token"])
        )
