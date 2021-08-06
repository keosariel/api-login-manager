
from flask import (
	Flask, 
	current_app,
	request,
	jsonify
)
import jwt
from functools import wraps
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from login_manager import APILoginManager
from utils import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
db  = SQLAlchemy(app)
login_manager = APILoginManager(app)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model):
    __tablename__ = 'user'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(20), nullable=False, unique=True)
    password      = db.Column(db.String(256), nullable=False)


@app.route("/login", methods=["POST"])
def login():
	username = request.json.get("username")
	password = request.json.get("password")

	if username is None or password is None:
		return jsonify({"message": "username and password required", "status":400}), 400

	user = User.query.filter_by(username=username).first()

	if user is None:
		return jsonify({"message": "user does not exists", "status": 400}), 400

	if user.password != password:
		return jsonify({"message": "Incorrect username and password", "status": 401}), 401

	# Generate token for user
	user_token = login_manager.get_token_for(user)

	return jsonify({"token": user_token})

@app.route("/signup", methods=["POST"])
def signup():
	username = request.json.get("username")
	password = request.json.get("password")

	if username is None or password is None:
		return jsonify({"message": "username and password required", "status":400}), 400

	user = User.query.filter_by(username=username).first()

	if user:
		return jsonify({"message": "username already exists", "status": 400}), 400

	# Note: it's safer you hash the password
	# This code is used for testing purposes
	user = User(
		username="keosariel",
		password="password"
	)
	db.session.add(user)
	db.session.commit()

	# Generate token for new user
	user_token = login_manager.get_token_for(user)

	return jsonify({"token": user_token})

@app.route("/", methods=["GET"])
@login_required
def home(current_user):
	return jsonify({"id": current_user.id, "username": current_user.username})

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)