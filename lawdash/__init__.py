import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc, desc
import json
from flask_cors import CORS

from Models import setup_db, Contact

from Auth import require_auth0

def create_app(test_config=None):
    app = Flask(__name__)
    
    setup_db(app)
    
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response
    
    @app.route("/")
    def helloWorld():
        return "Hello World!"
    
    @app.route('/contacts')
    @require_auth0('read:contacts')
    def contacts(payload):
        contacts = Contact.query.order_by(Contact.id).all()
        
        contacts_length = len(contacts)
        
        return jsonify({
            "size": contacts_length,
            "contacts": [contact.to_dict() for contact in contacts],
        })
    
    return app

