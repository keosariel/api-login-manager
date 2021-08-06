# API Login Manager
An simple implentation of `flask_login`  (login_required)

Use Case

```python
from flask import (
	Flask, 
	request,
	jsonify
)
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
	...
	# Generate token for user
	user_token = login_manager.get_token_for(user)

	return jsonify({"token": user_token})

@app.route("/signup", methods=["POST"])
def signup():
  """Creates a new user"""
  ...
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
```
