# Create your forms here.from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from app.models import User, Resto, MenuItem, ItemCategory

class RestoForm(FlaskForm):
  """Form for adding/updating a GroceryStore"""
  name = StringField('Resto name', validators=[DataRequired()])
  address = StringField('Address')
  category = SelectField('Category', choices=ItemCategory.choices())

def get_restos():
  return Resto.query