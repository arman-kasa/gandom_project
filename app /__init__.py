from flask import Flask
from mongoengine import connect

app = Flask(__name__)

connect("payments", host="127.0.0.1", port=27017)
