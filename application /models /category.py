from mongoengine import Document, IntField, StringField


class Category(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)

    def to_json(self):
        return {"id": self.id, "name": self.name}

    def populate(self, json):
        self.id = json["id"]
        self.name = json["name"]
