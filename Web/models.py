'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 13/07/2025
Ending //

'''
# Installing the necessary libraries
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# User model for authentication
class User(db.Model):
    """AI is creating summary for User

    Args:
        db ([type]): [description]
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Set password hash for the user
    def set_password(self, password):
        """AI is creating summary for set_password

        Args:
            password ([type]): [description]
        """
        self.password_hash = generate_password_hash(password)

    # Check if password matches the hash
    def check_password(self, password):
        """AI is creating summary for check_password

        Args:
            password ([type]): [description]

        Returns:
            [type]: [description]
        """
        return check_password_hash(self.password_hash, password)
