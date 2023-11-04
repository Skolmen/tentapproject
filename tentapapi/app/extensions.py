import os

from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials

# Initialize SQLAlchemy
db = SQLAlchemy()

# Get the current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Create the relative path to the file
file_path = os.path.join(current_dir, "../config/firebase-config-cred.json")

# Use the credentials
cred = credentials.Certificate(file_path)


default_app = firebase_admin.initialize_app(credential=cred)