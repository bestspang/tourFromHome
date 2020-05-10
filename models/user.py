import sqlite3
import datetime
from flask import current_app
from flask_user import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from db import db


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    username = db.Column(db.String(80))

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    # nodes = db.relationship('ActivateModel', backref=db.backref('users', lazy='dynamic'))
    # nodes = db.relationship('NodeModel', lazy='dynamic')


    # def __init__(self, username, password, email, email_confirmed_at):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #     self.email_confirmed_at = email_confirmed_at

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # THIS NEED TO BE DELETE !!!
    def json(self):
        return {'username': self.username, 'email': self.email}

    # def has_roles(self, *args):
    #     return set(args).issubset({role.name for role in self.roles})

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_or_create_user(cls, first_name, last_name, email, password, role=None):
        """ Find existing user or create new user """
        user = cls.query.filter(cls.email == email).first()
        if not user:
            user = cls(email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=current_app.user_manager.password_manager.hash_password(password),
                        active=True,
                        email_confirmed_at=datetime.datetime.utcnow())
            if role:
                user.roles.append(role)
            db.session.add(user)
        return user

# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes

    @classmethod
    def find_or_create_role(cls, name, label):
        """ Find existing role or create new role """
        role = cls.query.filter(cls.name == name).first()
        if not role:
            role = cls(name=name, label=label)
            db.session.add(role)
        return role

# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# # Define the User registration form
# # It augments the Flask-User RegisterForm with additional fields
# class MyRegisterForm(RegisterForm):
#     first_name = StringField('First name', validators=[
#         validators.DataRequired('First name is required')])
#     last_name = StringField('Last name', validators=[
#         validators.DataRequired('Last name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')

class UserDetail(db.Model):
    __tablename__ = 'user_details'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80))
    location = db.Column(db.String(80))
    dob = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store = db.relationship('UserModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE nane=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
