from flask import Flask, request , jsonify 
from mongoengine import (
    Document,
    IntField,
    StringField,
    ReferenceField,
    connect , 
    Q
)

app = Flask(__name__)

connect('payments', host='127.0.0.1', port=27017)

class Category(Document):
    id = IntField(primary_key = True)
    name = StringField(required = True )
    
    def to_json(self):
        return{
        "id" : self.id , 
        "name" : self.name 
        }
        
    def populate(self ,json):
        self.id = json["id"]
        self.name = json["name"]  
class Payment(Document):
    id = IntField(primary_key = True)
    price = IntField(required = True)
    name = StringField()
    category = ReferenceField(Category)
    
    def to_json(self):
        return{
        "id" : self.id,
        "price" : self.price,
        "name" : self.name , 
        "category" : self.category.to_json()
        }
        
    def populate(self ,json):
        self.id = json["id"]
        self.price = json["price"] 
        self.name = json["name"]  
        self.category = Category.objects.get(name=json["category"])      

@app.route('/')
def hello():
    return jsonify({"hello":"world"})

@app.route('/category/add' , methods=["POST"])
def add_category():  # sourcery skip: remove-unnecessary-else
    try:
        id = request.json["id"]
        name = request.json["name"]
        if Category.objects(Q(id = id)).first() is not None:
                return jsonify({"error" : "this id exists"}) , 404
        if Category.objects(Q(name = name)).first() is not None:
            return jsonify({"error" : "this name exists"}) , 404
        category = Category(id = id , name = name)
        category.save()
        return jsonify(category.to_json()), 201

    except Exception as ex:
        return f"Not Created!{ex}"
    
@app.route('/category/update/<int:id>' , methods=["PUT"])
def update_category(id):
    try:
        data = request.get_json()
        new_category = Category.objects(id=id)
        new_category.update(**data)
        
        return jsonify(new_category.to_json()) , 200
        
    except Exception as ex:
        return f"Not Updated!{ex}"

@app.route('/category/read' , methods=["GET"])
def category_read():
    try:
        category_all = Category.objects().all()
        all_category = [{"id" : c.id , "name" : c.name} for c in category_all]
        return jsonify(all_category), 200
        
    except Exception as ex:
        return f"Not Readed!{ex}"
    
@app.route('/payment/category/<int:id>')
def payment_category(id):
    selected = Payment.objects(Q(category = id)).all()
    all_payment = [{"id" : p.id,
        "price" : p.price,
        "name" : p.name , 
        "category" : {"id" : p.category.id , "name" : p.category.name}} for p in selected]
    return jsonify(all_payment) , 200

@app.route('/payment/add' , methods=["POST"])
def add_payment():  # sourcery skip: remove-unnecessary-else
    try:
        name = request.json["name"]
        id = request.json["id"]
        price = request.json["price"]
        category = request.json["category"]
        category_payment = Category.objects(id = category).first()
        if Category.objects(Q(id = category)).first() is None:
            return jsonify({"error" : "Not found this type of category!"}), 404
        if Payment.objects(Q(id = id)).first() is not None:
                return jsonify({"error" : "this id exists"})
        payment = Payment(id = id , name = name , price = price , category = category_payment).save()
        return jsonify(payment.to_json()), 201
    
    except Exception as ex:
        return f"Not Created!{ex}"

#404
@app.route('/payment/delete/<int:id>' , methods=["DELETE"])
def delete_payment(id):
    try:
        payments = Payment.objects(id =id).first()
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
        selected = Payment.objects().all()
        all_payment = [{"id" : p.id,
        "price" : p.price,
        "name" : p.name , 
        "category" : {"id" : p.category.id , "name" : p.category.name}} for p in selected]
        return jsonify(all_payment) , 200
        
    except Exception as ex:
        return f"Not Readed!{ex}"
    
@app.route('/payment/read_one' , methods=["GET"])
def read_one():
    try:
        payments = Payment.objects().first()
        return jsonify(payments.to_json()), 200
        
    except Exception as ex:
        return f"Not Readed!{ex}"

@app.route('/payment/read_lt/<int:price>' , methods=["GET"])
def read_lt(price):
    try:
        selected = Payment.objects(price__lte=price).all()
        all_payment = [{"id" : p.id,
        "price" : p.price,
        "name" : p.name , 
        "category" : {"id" : p.category.id , "name" : p.category.name}} for p in selected]
        return jsonify(all_payment) , 200

    except Exception as ex:
        return f"Not Readed!{ex}"
    
@app.route('/payment/read_gt/<int:price>' , methods=["GET"])
def read_gt(price):
    try:
        selected = Payment.objects(price__gte=price).all()
        all_payment = [{"id" : p.id,
        "price" : p.price,
        "name" : p.name , 
        "category" : {"id" : p.category.id , "name" : p.category.name}} for p in selected]
        return jsonify(all_payment) , 200

    except Exception as ex:
        return f"Not Readed!{ex}"
    
if __name__ == "__main__":
    app.debug = True
    app.run()

