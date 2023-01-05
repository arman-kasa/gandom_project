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
    try:
        data = request.get_json()
        paymant = Paymant()
        paymant.to_print(
            {
            "price": data["price"] ,
            "name": data["name"] 
            }
        )
        paymant.save()
        mycol.insert_one(paymant.to_json())
        return "Created!"
    except Exception as ex:
        return f"Not Created!{ex}"

@app.route('/paymant/delete')
def delete_paymant():
    try:
        myquery = { "name": "water" }
        x = mycol.delete_many(myquery)
        return f"{x.deleted_count} Delete"
    
    except Exception as ex:
        return f"Not Deleeted!{ex}"

@app.route('/paymant/update' , methods=["GET" , "POST"])
def update_paymant():
    try:
        myquery = { "name": "water" }
        newvalues = { "$set": { "name": "cake" } }
        x = mycol.update_many(myquery,newvalues)

        return "Updated!"
    except Exception as ex:
        return f"Not Updated!{ex}"

@app.route('/paymant/read' , methods=["GET"])
def read_paymant():
    try:
        for x in mycol.find():
            return str(x)
    except Exception as ex:
        return f"Not Readed!{ex}"
    
@app.route('/paymant/gt/<price>')
def read_paymant_gt(price):
    for doc in mycol.find({"price":{"$gt":price}}):
        return jsonify(doc)
    
if __name__ == "__main__":
    app.debug = True
    app.run()

