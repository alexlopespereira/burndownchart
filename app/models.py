
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date
from flask_security import UserMixin
import os
import importlib
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

TYPE_BANK_SLIP_PAYMENT = 2
TYPE_CREDIT_CARD_PAYMENT = 1
mname = os.environ['APP_SETTINGS'].split('.')[0]
cname = os.environ['APP_SETTINGS'].split('.')[1]
module = importlib.import_module(mname)
curr_config = getattr(module, cname)

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), index=True)
    hashpw = db.Column('password', db.String(250))
    email = db.Column('email', db.String(80), unique=True, index=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    registered_on = db.Column('registered_on', db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, email, password=None, name=None, admin=False, id=None):
        self.name = name
        if id:
            self.id = id
        if password:
            self.set_password(password)
        self.email = email
        self.admin = admin
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.hashpw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashpw, password)

    def to_json(self):
        json = {
            'url': self.get_url(),
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        return json

    def __repr__(self):
        return '<User %r>' % (self.name)
