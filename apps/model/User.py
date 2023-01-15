from mongoengine import Document, StringField ,IntField
import hashlib 
from flask import abort 
from apps import redisClient

class User(Document):
    username = StringField(primary_key=True, max_length=40)
    password = StringField(required=True)

    def to_json(self):
        return {
            "username": self.username
                    }

    def populate(self, json):
        self.username = json["username"]
        self.password = str(hashlib.md5(json["password"].encode()).hexdigest())
        
def get_user_by_token(token):
    try:
        username = redisClient.get(token).decode("utf-8")
        user = User.objects(username=username).first()
        return user.username
    except:
        abort(401)