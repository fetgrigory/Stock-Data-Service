'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 13/07/2025
Ending //

'''
# Installing the necessary libraries
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# User model for authentication
class User(db.Model):
    """AI is creating summary for User

    Args:
        db ([type]): [description]
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))
