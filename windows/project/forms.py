from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class CreditForm(FlaskForm):
    customer_id = IntegerField('Customer Id (1-300)', validators=[DataRequired()])
    submit = SubmitField('Calculate Risk')



