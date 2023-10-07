
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

from config import db

# Models go here!
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email.")
        return email
        
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Creature(db.Model):
    __tablename__ = "creatures"
    id = db.Column(db.Integer, primary_key=True)
    bug_name = db.Column(db.String, primary_key=True)
    image = db.Column(db.String)
    bug_description = db.Column(db.String)
   
    # Many to Many with BugBite model
    bug_bites = db.relationship("BugBite", secondary="biter", back_populates="creatures")

    bite_descriptions = association_proxy("bug_bites", "bite_description")

class BiteTreatment(db.Model):
    __tablename__ = "bite_treatments"
    id = db.Column(db.Integer, primary_key=True)
    treatment_plan = db.Column(db.String)

class BugBite(db.Model):
    __tablename__ = "bug_bites"
    id = db.Column(db.Integer, primary_key=True)
    bite_description = db.Column(db.String, nullable=False)
    __table_args__ = (
        CheckConstraint("LENGTH(bite_description) >= 10"),
    ) 
    symptoms = db.Column(db.String)
    severity_of_bite = db.Column(db.String)
    treatment_plan_id = db.Column(db.Integer, db.ForeignKey("bite_treatments.id"))
    
    # validate description length
    @validates("bite_description")
    def validate_description(self, key, bite_description):
        if len(bite_description) < 10:
            raise ValueError("Bite description must be at least 10 characters ")
        return bite_description
   
    # Many to Many with creature model
    creatures = db.relationship("Creature", secondary="biter", back_populates="creatures")
    
    #one to many with BiteTreatment model
    treatment_plan = db.relationship("BiteTreatment", back_populates="bug_bites")

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.String(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

class CreatureSchema(Schema):
    id = fields.Integer(dump_only=True)
    bug_name = fields.String(required=True)
    image = fields.String()
    bug_description = fields.String(required=True)


class BiteTreatmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    treatment_plan = fields.String()



class BugBiteSchema(Schema):
    id = fields.Integer(dump_only=True)
    bite_description = fields.String(required=True, validate=validate.Length(min=10))
    symptoms = fields.String()
    severity_of_bite = fields.String()
    treatment_plan_id = fields.Integer(required=True)
    creatures = fields.List(fields.String())