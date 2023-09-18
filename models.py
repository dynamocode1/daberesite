from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(600), nullable=False)  # Store the hashed passwor
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def data(self):
        return [
             self.id,
             self.username,
            self.email,
            self.password
        ]

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False,unique = True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(9000))
    def data(self):
         return {
            'id': self.id,
            'name': self.name,
            'description': product_item.description,
            'price': self.price,
            'image': self.image}
       

 

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

    def __init__(self, purchase_date, user_id, cart_id):
        self.purchase_date = purchase_date
        self.user_id = user_id
        self.cart_id = cart_id

    def data(self):
        return {
            'id': self.id,
            'purchase_date': self.purchase_date,
            'user_id': self.user_id,
            'cart_id': self.cart_id,
        }
class MyCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, user_id, product_id, quantity=1):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    second_phone = db.Column(db.String(20), nullable=True)  # Optional field
    products = db.Column(db.String(500), nullable=False)  # Storing product names as a comma-separated string
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.String(500))

