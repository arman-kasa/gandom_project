from flask import Flask, request, jsonify
from application.models import Category, Payment

app = Flask(__name__)


@app.route("/category", methods=["POST"])
def add_category():  # sourcery skip: remove-unnecessary-else
    try:
        data = request.get_json()
        category = Category()
        category.populate(data)
        if Category.objects(id=category.id).first() is not None:
            return jsonify({"error": "this id exists"}), 400
        if Category.objects(name=category.name).first() is not None:
            return jsonify({"error": "this name exists"}), 400
        category.save()
        return jsonify(category.to_json()), 201

    except Exception as ex:
        return f"Not Created!{ex}"


@app.route("/category/<int:id>", methods=["PUT"])
def update_category(id):
    try:
        data = request.get_json()
        new_category = Category.objects(id=id).first()
        new_category.update(**data)

        return jsonify(new_category.to_json()), 200

    except Exception as ex:
        return f"Not Updated!{ex}"


@app.route("/category", methods=["GET"])
def category_read():
    try:
        category_all = Category.objects()
        print(type(category_all))
        all_category = [c.to_json() for c in category_all]
        return jsonify(all_category), 200

    except Exception as ex:
        return f"Not Readed!{ex}"


@app.route("/payment/<int:category_id>")
def payment_category(category_id):
    selected = Payment.objects(category=category_id)
    all_payment = [p.to_json() for p in selected]
    return jsonify(all_payment), 200
