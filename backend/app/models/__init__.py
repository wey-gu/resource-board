#!/bin/env python
"""
models
"""
from app import db, ma, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Mapping Objects
# UserMixin gives us handy functions
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    mail = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<users('%s', '%s')>" % (self.id, self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    scale = db.Column(db.Integer)
    note = db.Column(db.String)
    high_availability = db.Column(db.Boolean)
    storage_backend = db.Column(db.String)
    hardware_type = db.Column(db.String)
    last_changed_at = db.Column(db.DateTime)
    last_changed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    state_name = db.Column(
        db.Integer, db.ForeignKey("states.name"), nullable=False)
    used_by = db.Column(db.String)

    def __repr__(self):
        return "<resources(\
            '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
            % (
                self.id, self.name, self.scale, self.note,
                self.high_availability, self.storage_backend,
                self.hardware_type, self.last_changed_at, self.last_changed_by,
                self.state_name, self.used_by)


class States(db.Model):
    """
    States will not be in large scale
    """
    name = db.Column(db.String, nullable=False, primary_key=True)
    resources = db.relationship(
        "Resources", backref='state', lazy=True)

    def __repr__(self):
        return "<states('%s')>" % (self.name)


class StatesSchema(ma.ModelSchema):
    class Meta:
        model = States


class ResourcesSchema(ma.ModelSchema):
    class Meta:
        model = Resources


class Resource_records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    res_name = db.Column(db.Integer, db.ForeignKey("resources.name"))
    record = db.Column(db.String)

    def __repr__(self):
        return "<resource_records('%s', '%s', '%s')>" % \
            (self.id, self.res_name, self.record)


class ResRecordsSchema(ma.ModelSchema):
    class Meta:
        model = Resource_records
