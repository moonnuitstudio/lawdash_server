from datetime import datetime
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError, Length, Optional

class BasicContactForm(Form):
    firstname = StringField(
        'firstname', validators=[DataRequired(), Length(-1,60)]
    )
    lastname = StringField(
        'lastname', validators=[DataRequired(), Length(-1,60)]
    )