from mongoengine import Document, IntField, StringField, ReferenceField , request 
from apps.model.category import Category
from apps.model.user import User
from app.controllers.User.user import get_user_by_token




class Payment(Document):
    id = IntField(primary_key=True)
    price = IntField(required=True)
    name = StringField()
    category = ReferenceField(Category)
    user = ReferenceField(User, required=True)

    

    def to_json(self):
        return {
            "id": self.id,
            "price": self.price,
            "name": self.name,
            "category": self.category.to_json(),
            "user":self.user.to_json()
        }

    def populate(self, json):
        self.id = json["id"]
        self.price = json["price"]
        self.name = json["name"]
        self.category = Category.objects.get(id=json["category"])
        self.user = User.objects.get(username=get_user_by_token(request.headers['token']))