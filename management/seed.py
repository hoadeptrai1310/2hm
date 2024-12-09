from .import db
from management.models import User, Product, Detail, Cart, Warehouse, TotalOrder, Order
from datetime import datetime

def seed_data():
    # user = User(user_id=1, user_name='Admin', password='sha256$QjodhlhrH0zvarWA$34be782d9f5e6b220e6752ee5e5c89c162e707ff964c6f4a4ccb810a8fc7d3e3', email='Thehieu0814@gmail.com',registration_date=datetime.now(),role='Admin')
    # cart = Cart(cart_id=1,user_id=1)
    # db.session.add(cart)
    # db.session.add(user)
    # db.session.commit()

    return None