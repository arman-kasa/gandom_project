from flask import request, jsonify , Blueprint
from application.model.Category import Category
from application.model.Payment import Payment

app_user = Blueprint("user", __name__, url_prefix="/user")

@app_user.route('/signup' , methods=["POST"])
def method_name():
    pass

@app_user.route('/login', methods=['POST'])
def method_name():
    pass

@app_user.route('', methods=['PUT'])
def update_password():
    pass

@app_user.route('', methods=['DELETE'])
def delete_acount():
    pass

@app_user.route('', methods=['GET'])
def get_payment():
    pass