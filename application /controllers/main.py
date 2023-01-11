from flask import Flask
from mongoengine import connect
from application.models import Category, Payment

app = Flask(__name__)

connect("payments", host="127.0.0.1", port=27017)

if __name__ == "__main__":
    app.debug = True
    app.run()
