from flask import Blueprint, render_template, request, jsonify
from models import User, Car, Salesperson, car_schema, all_cars_schema, salesperson_schema, all_sellers_schema, db
from helpers import token_required

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/testdata")
def testdata():
    return {"Planet": "Earth"}

@api.route("/carinventory", methods = ["POST"])
@token_required
def addcar(current_user_token):
    make = request.json["make"]
    model = request.json["model"]
    year_ = request.json["year_"]
    color = request.json["color"]
    price = request.json["price"]
    user_token = current_user_token.token
    
    print(f"BIG TESTER: {current_user_token}")

    car = Car(make, model, year_, color, price, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route("/carinventory", methods = ["GET"])
@token_required
def displaycarinv(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = all_cars_schema.dump(cars)
    return jsonify(response)

@api.route("carinventory/<id>", methods = ["GET"])
@token_required
def displaycar(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"ERROR": "Sorry, valid token required :("}), 401

@api.route("carinventory/<id>", methods = ["POST", "PUT"])
@token_required
def updatecar(current_user_token, id):
    car = Car.query.get(id)
    print("TEST")
    car.make = request.json["make"]
    car.model = request.json["model"]
    car.year_ = request.json["year_"]
    car.color = request.json["color"]
    car.price = request.json["price"]
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route("carinventory/<id>", methods = ["DELETE"])
@token_required
def deletecar(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route("sellers", methods = ["POST"])
@token_required
def addsalesperson(current_user_token):
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    phone = request.json["phone"]
    street = request.json["street"]
    city = request.json["city"]
    state = request.json["state"]
    zip = request.json["zip"]
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    salesperson = Salesperson(first_name, last_name, email, phone, street, city, state, zip, user_token = user_token)

    db.session.add(salesperson)
    db.session.commit()
    
    response = salesperson_schema.dump(salesperson)
    return jsonify(response)

@api.route("sellers", methods = ["GET"])
@token_required
def displaysellers(current_user_token):
    owner = current_user_token.token
    sellers = Salesperson.query.filter_by(user_token = owner).all()
    response = all_sellers_schema.dump(sellers)
    return jsonify(response)

@api.route("sellers/<id>", methods = ["GET"])
@token_required
def displaysalesperson(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        salesperson = Salesperson.query.get(id)
        response = salesperson_schema.dump(salesperson)
        return jsonify(response)
    else:
        return jsonify({"ERROR": "Sorry, valid token required :("}), 401
    
@api.route("sellers/<id>", methods = ["POST", "PUT"])
@token_required
def updatesalesperson(current_user_token, id):
    salesperson = Salesperson.query.get(id)

    salesperson.first_name = request.json["first_name"]
    salesperson.last_name = request.json["last_name"]
    salesperson.email = request.json["email"]
    salesperson.phone = request.json["phone"]
    salesperson.street = request.json["street"]
    salesperson.city = request.json["city"]
    salesperson.state = request.json["state"]
    salesperson.zip = request.json["zip"]
    salesperson.user_token = current_user_token.token

    db.session.commit()
    response = salesperson_schema.dump(salesperson)
    return jsonify(response)

@api.route("sellers/<id>", methods = ["DELETE"])
@token_required
def deletesalesperson(current_user_token, id):
    salesperson = Salesperson.query.get(id)
    db.session.delete(salesperson)
    db.session.commit()
    response = salesperson_schema.dump(salesperson)
    return jsonify(response)