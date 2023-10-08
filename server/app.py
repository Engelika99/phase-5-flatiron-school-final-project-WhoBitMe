#!/usr/bin/env python3

# Standard library imports
from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow.exceptions import ValidationError

# Remote library imports
from flask import request, jsonify
from flask_restful import Resource, Api

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Creature, BugBite, BiteTreatment
from schemas import UserSchema, CreatureSchema, BugBiteSchema, BiteTreatmentSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
ma = Marshmallow(app)
api = Api(app)


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'
#Get/search for current user
@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)

    if user:
        user_schema = UserSchema()
        user_json = user_schema.dump(user)

        return jsonify(user_json), 200
    else: 
        return jsonify({"message": "User not found"}), 404
  #Create new user  
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_schema = UserSchema()

    try:
        new_user = user_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    already_user = User.query.filter_by(email=new_user.email).first()
    if already_user:
        return jsonify({"message": "User already exists"}), 400    

    db.session.add(new_user)
    db.session.commit() 

    result = user_schema.dump(new_user)
    return jsonify({"message": "User created successfully", "user": result})  



if __name__ == '__main__':
    app.run(port=5555, debug=True)

