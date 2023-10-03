from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Creature(db.Model):
    __tablename__ = "creatures"
    id = db.Column(db.Integer, primary_key=True)
    bug_name = db.Column(db.String, primary_key=True)
    image = db.Column(db.String)
    
    bug_bites = db.relationship("BugBite", secondary="biter", back_populates="creatures")

class BugBite(db.Model):
    __tablename__ = "bug_bites"
    id = db.Column(db.Integer, primary_key=True)
    bite_description = db.Column(db.String)
    symptoms = db.Column(db.String)
    severity_of_bite = db.Column(db.String)

    creatures = db.relationship("Creature", secondary="biter", back_populate="creatures")

class BiteTreatment(db.Model):
    __tablename__ = "bite_treatments"
    id = db.Column(db.Integer, primary_key=True)
    treatment_plan = db.Column(db.String)
