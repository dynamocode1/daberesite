from models import *
from flask import session,request,redirect,url_for,Flask,jsonify
from models import db,User
import os
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin as ad
from blueprints import Views,Carts,Auth,Admin,Purchase
class App:
	app  = Flask(__name__)
	app.secret_key = os.urandom(32)
	app.register_blueprint(Views.view_bp)
	app.register_blueprint(Carts.cart_bp)
	app.register_blueprint(Auth.auth_bp)
	app.register_blueprint(Admin.admin_bp)
	app.register_blueprint(Purchase.purchase_bp)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	db.init_app(app)
	admin_view = ad(app, name='control', template_mode='bootstrap3')

	# Create view classes for each model
	class UsersView(ModelView):
	    column_list = ['id', 'name', 'email', 'password']
	

	# Register the views for each model with the Flask-Admin instance
	admin_view.add_view(UsersView(User, db.session))
	

	@app.route('/')
	def home():
		return redirect(url_for('views.home'))
	@app.route('/api')
	def api():
		a = Products.query.all()
		c = []
		for i in a:
			c.append(i.id)
		return jsonify({
			'test':c
			})