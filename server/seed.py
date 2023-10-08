#!/usr/bin/env python3

# Standard library imports
from random import choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db
from models import User, Creature, BugBite, BiteTreatment

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
        
        for _ in range(5): 
            user = User(username=fake.user_name(), email=fake.email(), password=fake.password())
            db.session.add(user)
            db.session.commit()

        for _ in range(5):
            creature = Creature(
                bug_name=rc(["Ant", "Spider", "Bee", "Tick"]),
                image=fake.image_url(),
                bug_description=fake.sentence(),
            )
            print(f"Inserting Creature: {creature}")
            db.session.add(creature)
            db.session.commit()

        for _ in range(5):
            bug_bite = BugBite(
                bite_description=fake.sentence(),
                symptoms=fake.paragraph(),
                severity_of_bite=rc(["Mild", "Moderate", "Severe"]),
            )
            db.session.add(bug_bite)
            db.session.commit()

            for _ in range(5):
                bite_treatment = BiteTreatment(
                treatment_plan=rc([
            "Wash with warm water and mild soap",
            "Apply antispetic cream",
            "Consult a doctor if symptoms persist",
            "Elevate the affected area"]),
            )
            db.session.add(bite_treatment)

            db.session.commit()

            print("Database seeded")

