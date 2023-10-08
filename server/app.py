#!/usr/bin/env python3

# Standard library imports
from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow.exceptions import ValidationError

# Remote library imports
from flask import request, jsonify
from flask_restful import Resource, Api, reqparse

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

# request treatment plan based on keywords received
@app.route('/search_creatures', methods=['GET'])
def search_creatures():
    keywords = request.args.get('keywords', '').split(',')
    creatures = Creature.query.filter(Creature.bug_description(f"%{'%'.join(keywords)}%")).all()
    creature_schema = CreatureSchema(many=True)
    creatures_data = creature_schema.dump(creatures)

    return jsonify({"creatures": creatures_data}), 200

# Use restful for bug bite
class BugBiteResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bite_description', type=str, required=True, help='Bite description')
        self.parser.add_argument('symptoms', type=str, help='Symptoms of the bite')
        self.parser.add_argument('severity_of_bite', type=str, help='Severity of the bite')
        self.parser.add_argument('treatment_plan_id', type=int, required=True, help='Treatment plan ID')

    def get(self, bug_bite_id):
        bug_bite = BugBite.query.get(bug_bite_id)

        if bug_bite:
            bug_bite_schema = BugBiteSchema()
            result = bug_bite_schema.dump(bug_bite)
            return jsonify(result), 200
        else:
            return jsonify({"message": "BugBite not found"}), 404
        
    def put(self,bug_bite_id):
        bug_bite = BugBite.query.get(bug_bite_id)

        if bug_bite:
            data = self.parser.parse_args()
            bug_bite_schema = BugBiteSchema()

            try:
                update_bug_bite = bug_bite_schema.load(data, instance=bug_bite, partial=True)
            except ValidationError as err:
                return jsonify(err.messages), 400
            
            db.session.commit()
            result = bug_bite_schema.dump(update_bug_bite)
            return jsonify({"message": "BugBite updated successfully", "bug_bite": result}), 200
        else:
            return jsonify({"message": "BugBite not found"}), 404
        
    def post(self):
        data = self.parser.parse_args()
        bug_bite_schema = BugBiteSchema()

        try:
            new_bug_bite = bug_bite_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        db.session.add(new_bug_bite)
        db.session.commit()
        result = bug_bite_schema.dump(new_bug_bite)
        return jsonify({"message": "BugBite created successfully", "bug_bite": result}), 201
        
    def delete(self, bug_bite_id):
        bug_bite = BugBite.query.get(bug_bite_id)

        if bug_bite:
            db.session.delete(bug_bite)
            db.session.commit()
            return jsonify({"message": "BugBite deleted successfully"}), 200
        else:
            return jsonify({"message": "BugBite not found"}), 404
        
api.add_resource(BugBiteResource, '/bug_bites/<int:bug_bite_id>')

#get bite treatment based on input of bite and creature
@app.route('/bite_treatments', methods=['GET'])
def get_bite_treatments_by_descriptions():
    bite_description = request.args.get('bite_description')
    creature_description = request.args.get('creature_description')
    query = BiteTreatment.query

    if bite_description:
        query = query.filter(BiteTreatment.bite_description == bite_description)

    if creature_description:
        query = query.join(BiteTreatment.creatures).filter(Creature.bug_description == creature_description)

    bite_treatments = query.all()
    bite_treatment_schema = BiteTreatmentSchema(many=True)
    result = bite_treatment_schema.dump(bite_treatments)
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)

