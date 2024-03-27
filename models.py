from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import secrets
import uuid

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(25), nullable = True)
    last_name = db.Column(db.String(25), nullable = True)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(), nullable = True, default = " ")
    token = db.Column(db.String(), default = " ", unique = True)
    g_auth_verify = db.Column(db.Boolean(), default = False)
    date_created = db.Column(db.DateTime(), nullable = False, default = datetime.now)

    def __init__(self, first_name, last_name, email, password = " ", token = " ", g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = self.g_auth_verify
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, your_password):
        self.hex_password = generate_password_hash(your_password)
        return self.hex_password
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def __repr__(self):
        return f"LOG: Successfully added the user {self.first_name} {self.last_name} ({self.email}) to the database :)"
    
class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(25))
    model = db.Column(db.String(25))
    year_ = db.Column(db.Integer)
    color = db.Column(db.String(25))
    price = db.Column(db.Double)
    user_token = db.Column(db.String, db.ForeignKey("user.token"))

    def __init__(self, make, model, year_, color, price, user_token, id=" "):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year_ = year_
        self.color = color
        self.price = price
        self.user_token = user_token
    
    def set_id(self):
        return (secrets.token_urlsafe())
    
    def __repr__(self):
        return "LOG: Successfully added a new car to the database."

class CarSchema(ma.Schema):
    class Meta:
        fields = ["id", "make", "model", "year_", "color", "price", "user_token"]

class Salesperson(db.Model):
    id = db.Column(db.String(), primary_key = True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(25))
    street = db.Column(db.String(100))
    city = db.Column(db.String(25))
    state = db.Column(db.String(25))
    zip = db.Column(db.Integer)
    user_token = db.Column(db.String, db.ForeignKey("user.token"))

    def __init__(self, first_name, last_name, email, phone, street, city, state, zip, user_token, id=" "):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.user_token = user_token

    def set_id(self):
        return str(secrets.token_urlsafe())
    
    def __repr__(self):
        return f"LOG: Successfully added a new salesperson to the team! :)"
    
class SalespersonSchema(ma.Schema):
    class Meta:
        fields = ["id", "first_name", "last_name", "email", "phone", "street", "city", "state", "zip", "user_token"]

car_schema = CarSchema()
all_cars_schema = CarSchema(many = True)

salesperson_schema = SalespersonSchema()
all_sellers_schema = SalespersonSchema(many = True)



