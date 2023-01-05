from flask import Flask, request , jsonify 
from mongoengine import (
    Document,
    IntField,
    StringField,
    connect
)

app = Flask(__name__)

connect('payments', host='127.0.0.1', port=27017)

class Payment(Document):
    id = IntField(primary_key = True)
    price = IntField(required = True)
    name = StringField()
    
    def to_json(self):
        return{
        "id" : self.id,
        "price" : self.price,
        "name" : self.name
        }
        
    def to_print(self ,json):
        self.id = json["id"]
        self.price = json["price"] 
        self.name = json["name"]        

@app.route('/')
def hello():
    return jsonify({"hello":"world"})

@app.route('/payment/add' , methods=["POST"])
def add_payment():
    try:
        data = request.get_json()
        payment = Payment(**data)
        payment.save()
        return jsonify(payment.to_json()), 201
    
    except Exception as ex:
        return f"Not Created!{ex}"

@app.route('/payment/delete/<int:id>' , methods=["DELETE"])
def delete_payment(id):
    try:
        payments = Payment.objects(id=id)
        payments.delete()
        return jsonify(payments.to_json()), 200
    
    except Exception as ex:
        return f"Not Deleeted!{ex}"

@app.route('/payment/update/<int:id>' , methods=["PUT"])
def update_payment(id):
    try:
        data = request.get_json()
        new_payment = Payment.objects(id=id)
        new_payment.update(**data)
        
        return jsonify(new_payment.to_json()) , 200
        
    except Exception as ex:
        return f"Not Updated!{ex}"

@app.route('/payment/read' , methods=["GET"])
def read_all():
    try:
        payments_all = Payment.objects()
        return jsonify(payments_all.to_json()), 200
        
    except Exception as ex:
        return f"Not Readed!{ex}"
    
@app.route('/payment/read_one_lt/<int:price>' , methods=["GET"])
def read_lt(price):
    try:
        payments_all = Payment.objects(price__lte=price)
        return jsonify(payments_all.to_json()), 200
        
    except Exception as ex:
        return f"Not Readed!{ex}"
    
@app.route('/payment/read_one_gt/<int:price>' , methods=["GET"])
def read_gt(price):
    try:
        payments_all = Payment.objects(price__gte=price)
        return jsonify(payments_all.to_json()), 200
        
    except Exception as ex:
        return f"Not Readed!{ex}"
    
if __name__ == "__main__":
    app.debug = True
    app.run()

