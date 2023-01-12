from mongoengine import Document, StringField ,IntField


class User(Document):
    id = IntField(primary_key=True)
    username = StringField(max_length=40)
    password = StringField(required=True)

    def to_json(self):
        return {
            "username": self.username,
            "password": self.password,
        }

    def populate(self, json):
        self.id = json["username"]
        self.price = json["password"]