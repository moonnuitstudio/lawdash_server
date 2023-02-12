import sys
import json
from flask_wtf.csrf import CSRFProtect
from flask import request, jsonify, abort
from Auth import require_auth0
from Models import Contact
from Form import BasicContactForm

def setup_contact_controller(app):
    csrf = CSRFProtect()

    with app.app_context():
        @app.route('/contacts')
        @require_auth0('read:contacts')
        def contacts(payload):
            contacts = Contact.query.order_by(Contact.id).all()
            
            contacts_length = len(contacts)
            
            return jsonify({
                "size": contacts_length,
                "contacts": [contact.to_dict() for contact in contacts],
            })
            
        @app.route('/contacts', methods=['POST'])
        @csrf.exempt
        @require_auth0('add:contacts')
        def add_contact(payload):
            try:
                form = BasicContactForm.from_json(request.json)
            
                if form.validate():
                    contact = Contact(
                        firstname = form.firstname.data,
                        lastname = form.lastname.data,
                    )
                    
                    contact.insert()
                    
                    lastest_contect = Contact.query.order_by(Contact.id.desc()).first()

                    return jsonify({
                        "success": True,
                        "contacts": [lastest_contect.to_dict()]
                    })
                else:
                    abort(400)
            except:
                print( sys.exc_info() )
                abort(500)
                
        @app.route('/contacts', methods=['DELETE'])
        @csrf.exempt
        @require_auth0('add:contacts')
        def delete_contacts(payload):
            try:
                data = request.json
                ids = data['ids']
                
                print(ids)
                
                return jsonify({
                    "success": True,
                })
            except:
                print( sys.exc_info() )
                abort(500)