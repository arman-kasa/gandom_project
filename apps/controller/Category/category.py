from apps.model import Category, Payment
from app.controllers.User.user import get_user_by_token
from flask import request, jsonify, Blueprint, abort
from mongoengine import Q


app_category = Blueprint("category", __name__, url_prefix="/category")


@app_category.route("", methods=["POST"])
def add_category():  # sourcery skip: remove-unnecessary-else
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])
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


@app_category.route("/<int:id>", methods=["PUT"])
def update_category(id):
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])
        data = request.get_json()
        new_category = Category.objects(Q(id=id) & Q(user=user))
        new_category.update_one(**data)

        return jsonify(new_category.to_json()), 200

    except Exception as ex:
        return f"Not Updated!{ex}"


@app_category.route("", methods=["GET"])
def category_read():
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])

        category_all = Category.objects(user=user).all()
        all_category = [{"id": c.id, "name": c.name} for c in category_all]
        return jsonify(all_category), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app_category.route("/<int:category_id>")
def payment_category(category_id):
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])

        selected = Payment.objects(Q(category=category_id) & Q(user=user)).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200
    except Exception as ex:
        return f"Not Readed!{ex}"
