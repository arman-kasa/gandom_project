from mongoengine import connect
import redis

connect("payments", host="127.0.0.1", port=27017)
redisClient = redis.StrictRedis(host="localhost", port=6379, db=0)


from flask import Flask

app = Flask(__name__)

from apps.controller.Category.category import app_category
from apps.controller.Payment.payment import app_payment
from apps.controller.User.user import app_user


app.register_blueprint(app_category)
app.register_blueprint(app_payment)
app.register_blueprint(app_user)
