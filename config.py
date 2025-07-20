import os
import secrets

class Config:
    # Get the database URL from the Render environment variable.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:qwerty@localhost:5432/expense_db'

    # Get the secret key from an environment variable for production.
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
