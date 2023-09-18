from flask import session,url_for,redirect
from functools import wraps
class user:
	def login_required(view_func):
		@wraps(view_func)
		def go_back(*args,**kwargs):
			if 'username' not in session:
				return redirect(url_for('auth.login'))
			else:
				pass
			return view_func(*args,**kwargs)
		return go_back
class admin:
	def login_required(view_func):
		@wraps(view_func)
		def go_back(*args,**kwargs):
			if 'admin' not in session:
				return redirect(url_for('dashboard.auth'))
			else:
				pass
			return view_func(*args,**kwargs)
		return go_back
