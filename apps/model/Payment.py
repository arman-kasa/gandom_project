from mongoengine import Document, IntField, StringField, ReferenceField
from apps.model import Category


class Payment(Document):
    id = IntField(primary_key=True)
    price = IntField(required=True)
    name = StringField()
    category = ReferenceField(Category)

    def to_json(self):
        return {
            "id": self.id,
            "price": self.price,
            "name": self.name,
            "category": self.category.to_json(),
        }

    def populate(self, json):
        self.id = json["id"]
        self.price = json["price"]
        self.name = json["name"]
        self.category = Category.objects.get(name=json["category"])
