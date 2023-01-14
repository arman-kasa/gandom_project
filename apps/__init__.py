from flask import Flask
from mongoengine import connect
from apps.controller.Category.category import app_category 
from apps.controller.Payment.payment import app_payment 


connect("payments", host="127.0.0.1", port=27017)

app = Flask(__name__)

app.register_blueprint(app_category)
app.register_blueprint(app_payment)



