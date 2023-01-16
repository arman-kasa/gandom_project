from mongoengine import Document, StringField
import hashlib


class User(Document):
    username = StringField(primary_key=True, max_length=40)
    password = StringField(required=True)

    def to_json(self):
        return {"username": self.username}

    def populate(self, json):
        self.username = json["username"]
        self.password = str(hashlib.md5(json["password"].encode()).hexdigest())
