from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Import your SQLAlchemy instance from db.py
from .db import db

class User(UserMixin, db.Model):
    """Model for user accounts."""
    
    __tablename__ = 'users'
    
    # Unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    # Username for login
    username = db.Column(db.String(150), unique=True, nullable=False)
    # Password hash for secure storage
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """Hash the password and set it to the password_hash field."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Student(db.Model):
    """Model for student records."""
    
    __tablename__ = 'students'

    # Unique identifier for each student
    id = db.Column(db.Integer, primary_key=True)
    # Student's name
    name = db.Column(db.String(100), nullable=False)
    # Student's age
    age = db.Column(db.Integer, nullable=False)
    # Student's unique identifier number (USN)
    usn = db.Column(db.String(20), unique=True, nullable=False)
    # Attendance percentage
    attendance = db.Column(db.Float, nullable=True)  # Optional, consider making nullable if not always required

    def __repr__(self):
        return f'<Student {self.name}>'
