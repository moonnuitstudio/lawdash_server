from flask import Flask, jsonify
from flask_cors import CORS

from Models import setup_db, Contact
from controllers.ContactController import setup_contact_controller
from Auth import require_auth0
import wtforms_json

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('Config')
    wtforms_json.init()
    setup_db(app)
    
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

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
    
    setup_contact_controller(app)

    # ERROR HANDLER
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "The server cannot or will not process the request due to an apparent client error."
        }), 400
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": error.description
        }), 500
    
    return app

