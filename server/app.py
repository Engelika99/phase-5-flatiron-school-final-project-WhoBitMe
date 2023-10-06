#!/usr/bin/env python3

# Standard library imports
from flask import Flask
from flask_migrate import Migrate

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Creature, BugBite, BiteTreatment


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

