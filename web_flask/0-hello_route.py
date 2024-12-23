#!/usr/bin/python3
"""
Simple Flask application serving a single endpoint.
"""
from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def home():
    """
    Handle the root route and return a greeting message.
    """
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

