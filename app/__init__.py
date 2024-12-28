from flask import Flask

app = Flask(__name__)

from app import server  # Import the server file where routes are defined
