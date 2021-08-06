from flask import (
	jsonify, 
	request, 
	current_app
)
from functools import wraps

def login_required(func):

	@wraps(func)
	def decorator(*args, **kwargs):
		auth_header   = request.headers.get('Authorization')
		error_message = current_app.login_manager.login_message

		if auth_header:
			try:
				# Expected format (Bearer TOKEN)
				token = auth_header.split(" ")[1]
			except IndexError:
				return jsonify(
					dict(
						status=401, 
						message=error_message
					)
				), 401

			valid, user_id = current_app.login_manager.decode_token(token)

			if valid:
				user = current_app.login_manager._user_callback(user_id)
				
				return func(*args, **kwargs, current_user=user)
			else:
				# Note: if not valid, user_id holds an error message
				error_message = user_id

		return jsonify(
			dict(
				status=401, 
				message=error_message
			)
		), 401

	return decorator

