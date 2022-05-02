# Create your models here.
from sqlalchemy_utils import URLType

from app.extensions import db
from app.utils import FormEnum
from flask_login import UserMixin

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    CAFE = 'Cafe'
    BAKERY = 'Bakery'
    RESTO = 'Resto'
    BAR = 'Bar'
    OTHER = 'Other'

class Resto(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('MenuItem', back_populates='resto')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    favorited_by = db.relationship('User', secondary='user_resto', back_populates='favorites')

class MenuItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    photo_url = db.Column(URLType)
    resto_id = db.Column(
        db.Integer, db.ForeignKey('resto.id'), nullable=False)
    resto = db.relationship('Resto', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    favorites = db.relationship('Resto', secondary='user_resto', back_populates='favorited_by')


user_resto = db.Table('user_resto',
    db.Column('resto_id', db.Integer, db.ForeignKey('resto.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)
