from __future__ import annotations
from . import db


class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    registration_date = db.Column(db.Date, unique=False)

    def __init__(self, name, password, registration_date):
        self.name, self.password, self.registration_date = name, password, registration_date
