from management import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime 
from sqlalchemy import LargeBinary
import uuid

class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Chuyển thành chữ thường

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone_number = db.Column(db.Integer)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role = db.Column(db.String(20), default='user')
    
    orders = db.relationship('Order', backref='user', lazy=True)
    carts = db.relationship('Cart', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.user_name}', '{self.email}')"
    def get_id(self):
        return str(self.user_id)

class Order(db.Model):
    __tablename__ = 'orders'  # Chuyển thành chữ thường
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(30))
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String(40))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.Integer)

    total_order = db.relationship('TotalOrder', lazy=True)
    def __repr__(self):
        return f"Order('{self.user_id}')"

class Cart(db.Model):
    __tablename__ = 'carts'  # Chuyển thành chữ thường
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    products = db.relationship('Product', backref='cart', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'  # Chuyển thành chữ thường
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.cart_id'), nullable=False)
    name_product = db.Column(db.String(200))
    price = db.Column(db.DECIMAL(precision=12, scale=2)) 
    quantity = db.Column(db.Integer)
    image = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    auto_imei = db.Column(db.String(36), unique=True, nullable=True)

    details = db.relationship('Detail', backref='product', lazy=True)
    warehouses = db.relationship('Warehouse', backref='product', lazy=True)

    def __init__(self, cart_id, name_product, price, quantity, image):
        self.cart_id = cart_id
        self.name_product = name_product
        self.price = price
        self.quantity = quantity
        self.image = image
        self.auto_imei = self.generate_auto_imei()

    def generate_auto_imei(self):
        return str(uuid.uuid4())
        
class Detail(db.Model):
    __tablename__ = 'details'  # Chuyển thành chữ thường
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False, unique=True)
    type_product = db.Column(db.String(255))
    color_product = db.Column(db.String(20))
    size_product = db.Column(db.String(20))
    producer = db.Column(db.String(255))
    describe = db.Column(db.String(2000))
    extend = db.Column(db.String(2000))

class TotalOrder(db.Model):
    __tablename__ = 'total_orders'  # Chuyển thành chữ thường
    total_order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_order = db.Column(db.DECIMAL(precision=12, scale=2)) 
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)

class Warehouse(db.Model):
    __tablename__ = 'warehouses'  # Chuyển thành chữ thường
    warehouse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_warehouse = db.Column(db.DECIMAL(precision=12, scale=2)) 
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=True)
