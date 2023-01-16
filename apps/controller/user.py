from flask import request, jsonify, Blueprint, abort
from mongoengine import Q
import hashlib
from datetime import timedelta
import uuid


from apps.model.category import Category
from apps.model.payment import Payment
from apps.model.user import User

from apps import redisClient


app_user = Blueprint("user", __name__, url_prefix="/user")


@app_user.route("/signup", methods=["POST"])
def sign_up():
    data = request.get_json()
    user = User()
    user.populate(data)
    if User.objects(Q(username=user.username)).first() is not None:
        return jsonify({"error": "this username exists"}), 403
    user.save()
    return jsonify(user.to_json()), 201


@app_user.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if (
        User.objects(
            username=data["username"],
            password=str(hashlib.md5(data["password"].encode()).hexdigest()),
        ).first()
        is None
    ):
        abort(401)
    token = str(uuid.uuid4())
    redisClient.set(token, data["username"])
    redisClient.expire(token, timedelta(hours=3))
    return jsonify({"token": token, "message": "login successful"}), 200


@app_user.route("", methods=["PUT"])
def update_password():
    if "token" not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers["token"])

    user_pass = User.objects(username=user).first()

    data = request.get_json()
    old_password = str(hashlib.md5(data["old_password"].encode()).hexdigest())
    new_password = str(hashlib.md5(data["new_password"].encode()).hexdigest())
    if user_pass.password != old_password:
        abort(401)
    User.objects(username=user).update(password=new_password)
    return jsonify({"username": user, "message": "password changed"}), 200


@app_user.route("", methods=["DELETE"])
def delete_acount():
    if "token" not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers["token"])

    user_pass = User.objects(username=user).first()

    data = request.get_json()

    password = str(hashlib.md5(data["password"].encode()).hexdigest())

    if user_pass.password != password:
        abort(401)
    query = Category.objects(user=user)
    for category in query:
        Payment.objects(category=category).delete()
        category.delete()
    user_pass.delete()
    return jsonify({"message": "DELETED"}), 200
