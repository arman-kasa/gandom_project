from flask import Flask, request, jsonify , abort 
from mongoengine import Document, IntField, StringField, ReferenceField , connect , Q 
import hashlib
import redis
from datetime import timedelta
import uuid

app = Flask(__name__)

connect("payments", host="127.0.0.1", port=27017)
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)


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
        

class Category(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)
    user = ReferenceField(User, required=True)


    def to_json(self):
        return {
            "id": self.id, 
            "name": self.name,
        }

    def populate(self, json):
        self.id = json["id"]
        self.name = json["name"]
        self.user = User.objects.get(username=get_user_by_token(request.headers['token']))

        
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

def get_user_by_token(token):
    try:
        username = redisClient.get(token).decode("utf-8")
        user = User.objects(username=username).first()
        return user.username
    except:
        abort(401)
        
@app.route("/category", methods=["POST"])
def add_category():  # sourcery skip: remove-unnecessary-else
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])
        data = request.get_json()
        category = Category()
        category.populate(data)
        if Category.objects(Q(id=category.id) & Q(user=user)).first() is not None:
            return jsonify({"error": "this id exists"}), 400
        if Category.objects(Q(name=category.name) & Q(user=user)).first() is not None:
            return jsonify({"error": "this name exists"}), 400
        category.save()
        return jsonify(category.to_json()), 201

    except Exception as ex:
        return f"Not Created!{ex}"



@app.route("/category/<int:id>", methods=["PUT"])
def update_category(id):
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])
        data = request.get_json()
        new_category = Category.objects(Q(id=id) & Q(user=user))
        new_category.update_one(**data)

        return jsonify(new_category.to_json()), 200

    except Exception as ex:
        return f"Not Updated!{ex}"


@app.route("/category", methods=["GET"])
def category_read():
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])

        category_all = Category.objects(user = user).all()
        all_category = [{"id": c.id, "name": c.name} for c in category_all]
        return jsonify(all_category), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app.route("/payment/cat/<int:category_id>", methods=["GET"])
def payment_category(category_id):
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])

        selected = Payment.objects(Q(category=category_id) & Q(user=user)).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200
    except Exception as ex:
        return f"Not Readed!{ex}"

@app.route("/payment", methods=["POST"])
def add_payment():
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token']) 
        # sourcery skip: remove-unnecessary-else
        data = request.get_json()
        payment = Payment()
        payment.populate(data)
        if Category.objects(Q(id=payment.category.id) & Q(user=user)).first() is None:
            return jsonify({"error": "Not found this type of category!"}), 404
        if Payment.objects(Q(id=payment.id) & Q(user=user)).first() is not None:
            return jsonify({"error": "this id exists"}) , 409
        payment.save()
        return jsonify(payment.to_json()), 201
    except Exception as ex:
        return f"Not Added!{ex}"


@app.route("/payment/<int:id>", methods=["DELETE"])
def delete_payment(id):
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])

        payments = Payment.objects(Q(id=id) & Q(user=user)).first()
        if payments is None:
            return jsonify({"error": "item not found"}), 404
        payments.delete()
        return jsonify(payments.to_json(), "DELETED"), 200
    except Exception as ex:
        return f"Not Deleted!{ex}"


@app.route("/payment/<int:id>", methods=["PUT"])
def update_payment(id):
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])

        if Payment.objects(Q(id=id) & Q(user=user)).first() is None:
            return jsonify({"error": "doent exist thid id"}) , 404
        data = request.get_json()
        category = Category.objects(id=data["category"]).first()
        Payment.objects(Q(id=id) & Q(user=user)).update_one(name=data["name"] , price=data["price"] , category = category)

        return jsonify({"message":"payment updated"}), 200
    except Exception as ex:
        return f"Not Updated!{ex}"

@app.route("/payment", methods=["GET"])
def read_all():
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])

        selected = Payment.objects(user=user).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200



@app.route("/payment/<int:id>", methods=["GET"])
def read_one(id):
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])
        payments = Payment.objects(Q(id=id) & Q(user=user)).first()
        return jsonify(payments.to_json()), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app.route("/payment/lt/<int:price>", methods=["GET"])
def read_lt(price):
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])
        selected = Payment.objects(Q(price__lte=price) & Q(user = user)).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app.route("/payment/gt/<int:price>", methods=["GET"])
def read_gt(price):
    try:
        if 'token' not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers['token'])
        selected = Payment.objects(Q(price__gte=price) & Q(user = user)).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app.route('/user/signup' , methods=["POST"])
def sign_up():
    data = request.get_json()
    user = User()
    user.populate(data)
    if User.objects(Q(username=user.username)).first() is not None:
            return jsonify({"error": "this username exists"}), 403
    user.save()
    return jsonify(user.to_json()) , 201

@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    if User.objects(username=data["username"], password=str(hashlib.md5(data["password"].encode()).hexdigest())).first() is None:
        abort(401)
    token = str(uuid.uuid4())
    redisClient.set(token, data["username"])
    redisClient.expire(token, timedelta(hours=3))
    return jsonify({"token": token, "message": "login successful"}), 200

@app.route('/user', methods=['PUT'])
def update_password():
    if 'token' not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers['token'])

    user_pass = User.objects(username=user).first()

    data = request.get_json()
    old_password = str(hashlib.md5(data["old_password"].encode()).hexdigest())
    new_password = str(hashlib.md5(data["new_password"].encode()).hexdigest())
    if user_pass.password != old_password:
        abort(401)
    User.objects(username=user).update(password=new_password)
    return jsonify({"username": user, "message": "password changed"}), 200


@app.route('/user', methods=["DELETE"])
def delete_acount():
    if 'token' not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers['token'])

    user_pass = User.objects(username=user).first()
    password = str(hashlib.md5(request.get_json["password"].encode()).hexdigest())

    if user_pass.password != password:
        abort(401)
    query = Category.objects(user=user)
    for category in query:
        Payment.objects(category=category).delete()
        category.delete()
    user.delete()
    return jsonify({"message": "DELETED"}), 200

if __name__ == "__main__":
    app.debug = True
    app.run()
