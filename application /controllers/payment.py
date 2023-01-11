from flask import Flask, request, jsonify
from application.models import Category, Payment

app = Flask(__name__)


@app.route("/payment", methods=["POST"])
def add_payment():  # sourcery skip: remove-unnecessary-else
    try:
        data = request.get_json()
        payment = Payment()
        payment.populate(data)
        if Category.objects(id=data.category.id).first() is None:
            return jsonify({"error": "Not found this type of category!"}), 404
        if Payment.objects(id=id).first() is not None:
            return jsonify({"error": "this id exists"})
        payment.save()
        return jsonify(payment.to_json()), 201

    except Exception as ex:
        return f"Not Created!{ex}"


@app.route("/payment/<int:id>", methods=["DELETE"])
def delete_payment(id):
    try:
        payments = Payment.objects(id=id).first()
        payments.delete()
        return jsonify(payments.to_json()), 200

    except Exception as ex:
        return f"Not Deleeted!{ex}"


@app.route("/payment/<int:id>", methods=["PUT"])
def update_payment(id):
    try:
        data = request.get_json()
        new_payment = Payment.objects(id=id)
        new_payment.update(**data)

        return jsonify(new_payment.to_json()), 200

    except Exception as ex:
        return f"Not Updated!{ex}"


@app.route("/payment", methods=["GET"])
def read_all():
    try:
        selected = Payment.objects().all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app.route("/payment/<int:id>", methods=["GET"])
def read_one(id):
    try:
        payments = Payment.objects(id=id).first()
        return jsonify(payments.to_json()), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app.route("/payment/lt/<int:price>", methods=["GET"])
def read_lt(price):
    try:
        selected = Payment.objects(price__lte=price).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app.route("/payment/gt/<int:price>", methods=["GET"])
def read_gt(price):
    try:
        selected = Payment.objects(price__gte=price).all()
        all_payment = [p.to_json() for p in selected]
        return jsonify(all_payment), 200

    except Exception as ex:
        return f"Not Readed!{ex}"
