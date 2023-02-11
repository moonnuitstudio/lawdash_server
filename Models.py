import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
from flask_migrate import Migrate

DB_IP = os.getenv("DB_IP")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

database_path = "postgresql://{}:{}@{}:{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_IP, DB_PORT, DB_NAME)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    with app.app_context():
        db.app = app
        db.init_app(app)
        migrate = Migrate(app, db)
        db.create_all()
        
        
class Contact(db.Model):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(60))
    middlename = Column(String(30))
    lastname = Column(String(60))
    email = Column(String(200))
    dayphone = Column(String(15))
    mobilenumber = Column(String(15))
    worknumber = Column(String(15))
    
    def __init__(self, type):
        self.type = type
        
    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'middlename': self.middlename,
            'lastname': self.lastname,
            'email': self.email,
            'dayphone': self.dayphone
        }