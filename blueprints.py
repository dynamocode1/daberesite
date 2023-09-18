import bleach
from flask import Blueprint, url_for, redirect, request, session, render_template, flash, jsonify
from decorators import user, admin
from flask_bcrypt import Bcrypt
import cloudinary
import cloudinary.uploader
import cloudinary.api
from models import *
# from models import _Cart
from asset import html_tags

cloudinary.config(
    cloud_name='dvnflgqs2',
    api_key='975551641336967',
    api_secret='l12W5dcvd3JvHDr7Hi-Wyx9Q17c'
)

bcrypt = Bcrypt()

class Views:
    view_bp = Blueprint('views', __name__, url_prefix='/home')

    @view_bp.route('/')
    def home():
        products = Products.query.all()
        print(products)
        return render_template('home.html', products=products)

    @view_bp.route('/about')
    def about():
        return render_template('about.html')

    @view_bp.route('/contact')
    def contact():
        return render_template('contact.html')
    @view_bp.route('/crypto')
    def crypto():
    	return render_template('crypto.html')

class Carts:
    cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

    @cart_bp.route('/')
    @user.login_required
    def cart():
    	user_id = session['username']
    	cart_items = MyCart.query.filter_by(user_id=user_id).all()
    	cart_with_details = []
    	for cart_item in cart_items:
    		product_item = Products.query.filter_by(id=cart_item.product_id).first()  # Retrieve product by ID
    		if product_item:
    			cart_with_details.append({
		                'product': {
		                    'id': product_item.id,
		                    'name': product_item.name,
		                    'description': product_item.description,
		                    'price': product_item.price,
		                    'image': product_item.image
		                },
		                'quantity': cart_item.quantity,
		                'id': cart_item.id
		            })
    		else:
    			cart_with_details.append({
		                'product': None,
		                'quantity': cart_item.quantity,
		                'id': cart_item.id
		            })
    	return render_template('cart.html', data=cart_with_details,val = len(cart_with_details))


    @cart_bp.route('/delete_item/<int:item_id>')
    @user.login_required
    def delete_item(item_id):
        item_to_delete = MyCart.query.get_or_404(item_id)

        try:
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Item deleted successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the item', 'error')
        finally:
            db.session.close()

        return redirect(url_for('cart.cart'))

class Auth:
    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

    @auth_bp.route('/')
    def login():
        return render_template('login.html')

    @auth_bp.route('/signup')
    def signup():
        return render_template('signup.html')

    @auth_bp.route('/confirm_signup', methods=['GET', 'POST'])
    def signup_confirmed():

        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()
            if existing_user:
                flash('User Already Exists')
                return redirect(url_for('auth.signup'))
            elif existing_email:
                flash('Email in use')
                return redirect(url_for('auth.signup'))
            else:
                new_user = User(username, email, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect(url_for('cart.cart'))

    @auth_bp.route('/confirm_login', methods=['GET', 'POST'])
    def login_confirmed():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if not user:
                flash('No such user')
                return redirect(url_for('auth.login'))
            elif not bcrypt.check_password_hash(user.data()[3], password):
                flash('Incorrect Password','error')
                return redirect(url_for('auth.login'))
            else:
                session['username'] = username
                return redirect(url_for('cart.cart'))

    @auth_bp.route('/logout')
    def logout():
        session.pop('username')

class Admin:
    admin_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

    @admin_bp.route('/')
    def index():
        return redirect(url_for('dashboard.product'))

    @admin_bp.route('/login', methods=['GET', 'POST'])
    def login():
        name = request.form.get('username')
        password = request.form.get('password')
        if name == 'dynamocode1' and password == 'winnergenuissystem':
            session['admin'] = name
            return redirect(url_for('dashboard.product'))
        else:
            flash('error')
            return redirect(url_for('dashboard.auth'))

    @admin_bp.route('/dashboard/user/dynamocode')
    @admin.login_required
    def product():
        products = Products.query.all()
        print(products)
        return render_template('product.html', products=products)

    @admin_bp.route('/verify')
    def auth():
        return render_template('adminlogin.html')

    @admin_bp.route('/delete_order/<int:order_id>')
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            flash('Order deleted successfully', 'success')
        else:
            flash('Order not found', 'error')
        return redirect(url_for('dashboard.view_orders'))

    @admin_bp.route('/view_orders')
    def view_orders():
        orders = Order.query.all()
        return render_template('adminOrder.html', orders=orders)

    @admin_bp.route('/add_product', methods=['GET', 'POST'])
    @admin.login_required
    def add_product():
        name = request.form.get('name')
        price = float(request.form.get('price'))

        # Specify allowed HTML tags including bold and italic
        html_tags = [
            'a',    # Anchor (for linking)
            'p',    # Paragraph
            'br',   # Line Break
            'ul',   # Unordered List
            'ol',   # Ordered List
            'li',   # List Item
            'h1',   # Heading 1
            'h2',   # Heading 2
            'h3',   # Heading 3
            'em',   # Emphasis (italic)
            'strong'  # Strong (bold)
        ]

        description = bleach.clean(request.form.get('description'), tags=html_tags, attributes={})
        image = request.files['image']

        result = cloudinary.uploader.upload(image)

        new_product = Products(name=name, price=price, description=description, image=result['secure_url'])

        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully', 'success')

        return redirect(url_for('dashboard.product'))

    @admin_bp.route('/delete/<id>')
    @admin.login_required
    def delete(id):
        product = Products.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()
        flash('User deleted successfully', 'success')
        return redirect(url_for('dashboard.index'))
    @admin_bp.route('/send', methods=['GET', 'POST'])
    def contact_form():
    	if request.method == 'POST':
    		name = request.form.get('name')
    		email = request.form.get('email')
    		message = request.form.get('message')
    		new_message = ContactMessage(name=name, email=email, message=message)
    		db.session.add(new_message)
    		db.session.commit()
    		return redirect(url_for('views.home'))

class Purchase:
    purchase_bp = Blueprint('purchase', __name__, url_prefix='/purchase')

    @purchase_bp.route('/add_to_cart/<id>')
    @user.login_required
    def add_to_cart(id):

        user_id = session['username']
        user = User.query.filter_by(username=user_id).first()  # Replace with the actual user ID
        product_id = id
        cart_item = MyCart(user_id, product_id=id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()

        data = {
            'success': 'Added successfully'
        }
        return redirect(url_for('views.home'))

    @purchase_bp.route('/order')
    @user.login_required
    def order():
    	
    	return render_template('order.html')

    @purchase_bp.route('/')
    def index():
        return render_template('index.html')

    @purchase_bp.route('/submit_order', methods=['POST'])
    @user.login_required
    def submit_order():
        item = []
        items = str(db.session.query(MyCart.product_id).all()[0])
        get = MyCart.query.filter_by()
        if request.method == 'POST':
            address = request.form['address']
            phone = request.form['phone']
            second_phone = request.form['secondPhone']
            products = item
            order = Order(address=address, phone=phone, second_phone=second_phone, products=items)
            db.session.add(order)
            username = session['username']
            MyCart.query.filter_by(user_id=username).delete()
            db.session.commit()
            flash('Order placed successfully', 'success')
        
            return redirect(url_for('views.home'))
