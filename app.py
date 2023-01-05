from flask import Flask, render_template , request , jsonify 
import pymongo
from mongoengine import (
    Document,
    IntField,
    StringField,
    connect
)

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["accounter"]
mycol = mydb["paymants"]
connect('mydb', host='127.0.0.1', port=27017)

class Paymant(Document):
    price = StringField(required = True)
    name = StringField()
    
    def to_json(self):
        return{
        "price" : self.price,
        "name" : self.name
        }
        
    def to_print(self ,json):
            self.price = json["price"] 
            self.name = json["name"]        

@app.route('/')
def hello():
    return jsonify({"hello":"world"})

@app.route('/paymant/add' , methods=["POST" , "GET"])
def add_paymant():
    data = request.get_json()
    paymant = Paymant()
    paymant.to_print(
        {
        "price": data["price"] ,
        "name": data["name"] 
        }
    )
    paymant.save()
    return jsonify(paymant.to_json()) ,201  

@app.route('/paymant/delete')
def delete_paymant():
    
    myquery = { "name": "water" }
    x = mycol.delete_many(myquery)
    
    return f"{x.deleted_count} Delete"

@app.route('/paymant/update')
def update_paymant():
    myquery = { "name": "water" }
    newvalues = { "$set": { "name": "juice" } }
    x = mycol.update_many(myquery,newvalues)

    return f"{x.modified_count} Update"

@app.route('/paymant/read')
def read_paymant():
    for x in mycol.find():
        return x

    
if __name__ == "__main__":
    app.debug = True
    app.run()

