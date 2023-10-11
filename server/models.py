from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
from flask_login import UserMixin

from config import db

# Models go here!
biter = db.Table(
    "biter",
    db.Column("creature_id", db.Integer, db.ForeignKey("creatures.id")),
    db.Column("bug_bite_id", db.Integer, db.ForeignKey("bug_bites.id")),
    db.PrimaryKeyConstraint("creature_id", "bug_bite_id")
    )

class User(db.Model, UserMixin):
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

#one-to-many with bugbite
    bug_bites = db.relationship("BugBite", back_populates="user")    
    

class Creature(db.Model):
    __tablename__ = "creatures"
    id = db.Column(db.Integer, primary_key=True)
    bug_name = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    bug_description = db.Column(db.String)

    def __repr__(self):
        return f"<Creature(id={self.id}, bug_name='{self.bug_name}', image='{self.image}', bug_description='{self.bug_description}')>"
   
    # Many to Many with BugBite model
    bug_bites = db.relationship("BugBite", secondary="biter", back_populates="creatures")
    
    bite_descriptions = association_proxy("bug_bites", "bite_description")

class BiteTreatment(db.Model):
    __tablename__ = "bite_treatments"
    id = db.Column(db.Integer, primary_key=True)
    treatment_plan = db.Column(db.String)

    bug_bites = db.relationship("BugBite", back_populates="treatment_plan")

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
    
    #many-to-one with user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="bug_bites")
   

    # Many to Many with creature model
    creatures = db.relationship("Creature", secondary="biter", back_populates="bug_bites")
    
    #one to many with BiteTreatment model
    treatment_plan = db.relationship("BiteTreatment", back_populates="bug_bites")



