from flask import request, jsonify, Blueprint, abort
from mongoengine import Q
from apps.model.category import Category
from apps.model.payment import Payment
from apps.utils import get_user_by_token


app_payment = Blueprint("payment", __name__, url_prefix="/payment")


@app_payment.route("", methods=["POST"])
def add_payment():  # sourcery skip: remove-unnecessary-else
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])
        # sourcery skip: remove-unnecessary-else
        data = request.get_json()
        payment = Payment()
        payment.populate(data)
        if Category.objects(Q(id=payment.category.id) & Q(user=user)).first() is None:
            return jsonify({"error": "Not found this type of category!"}), 404
        if Payment.objects(Q(id=payment.id) & Q(user=user)).first() is not None:
            return jsonify({"error": "this id exists"}), 409
        payment.save()
        return jsonify(payment.to_json()), 201
    except Exception as ex:
        return f"Not Added!{ex}"


@app_payment.route("/<int:id>", methods=["DELETE"])
def delete_payment(id):
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])

        payments = Payment.objects(Q(id=id) & Q(user=user)).first()
        if payments is None:
            return jsonify({"error": "item not found"}), 404
        payments.delete()
        return jsonify(payments.to_json(), "DELETED"), 200
    except Exception as ex:
        return f"Not Deleted!{ex}"


@app_payment.route("/<int:id>", methods=["PUT"])
def update_payment(id):
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])

        if Payment.objects(Q(id=id) & Q(user=user)).first() is None:
            return jsonify({"error": "doent exist thid id"}), 404
        data = request.get_json()
        category = Category.objects(id=data["category"]).first()
        Payment.objects(Q(id=id) & Q(user=user)).update_one(
            name=data["name"], price=data["price"], category=category
        )

        return jsonify({"message": "payment updated"}), 200
    except Exception as ex:
        return f"Not Updated!{ex}"


@app_payment.route("", methods=["GET"])
def read_all():
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])

        selected = Payment.objects(user=user).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200
    except Exception as ex:
        return f"Not Readed!{ex}"


@app_payment.route("/<int:id>", methods=["GET"])
def read_one(id):
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])
        payments = Payment.objects(Q(id=id) & Q(user=user)).first()
        return jsonify(payments.to_json()), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app_payment.route("/lt/<int:price>", methods=["GET"])
def read_lt(price):
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])
        selected = Payment.objects(Q(price__lte=price) & Q(user=user)).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app_payment.route("/gt/<int:price>", methods=["GET"])
def read_gt(price):
    try:
        if "token" not in request.headers:
            abort(401)
        user = get_user_by_token(request.headers["token"])
        selected = Payment.objects(Q(price__gte=price) & Q(user=user)).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200

    except Exception as ex:
        return f"Not Readed!{ex}"
