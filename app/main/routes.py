from flask import Blueprint, request, render_template, redirect, url_for, flash
import flask_login
from app.main.forms import RestoForm, CommentForm
from app.models import Resto, User, MenuItem, Review
from app.extensions import app, db
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)

# Create your routes here.
@main.route('/')
def index():
  restos = Resto.query.all()
  return render_template('home.html', restos = restos)

@main.route('/users')
def users():
  users = User.query.all()
  return render_template('users.html', users=users)

@main.route('/user/<user_id>')
def user_details(user_id):
  user = User.query.get(user_id)
  return render_template('user_detail.html', user=user)

@main.route('/favorite/<resto_id>', methods=['POST'])
@login_required
def favorite(resto_id):
  user = flask_login.current_user
  resto = Resto.query.get(resto_id)
  user.favorites.append(resto)
  db.session.add(user)
  db.session.commit()
  flash('resto added')
  
  return redirect(url_for('main.favorites'))

@main.route('/favorites')
@login_required
def favorites():
  user = flask_login.current_user
  return render_template('favorites_detail.html', user=user)

@main.route('/new_resto', methods=['GET', 'POST'])
@login_required
def new_resto():
  form = RestoForm()

  if form.validate_on_submit():
    resto = Resto(
      name = form.name.data,
      address = form.address.data,
      category = form.category.data,
      created_by = flask_login.current_user
    )
    db.session.add(resto)
    db.session.commit()

    flash('Resto added!')
    return redirect(url_for('main.index'))

  return render_template('new_resto.html', form=form)
 
@main.route('/resto/<resto_id>', methods=['GET', 'POST'])
def resto_detail(resto_id):
  resto = Resto.query.get(resto_id)
  form = RestoForm(obj=resto)
  comment_form = CommentForm()

  if comment_form.validate_on_submit():
    review = Review(
      reviewer = flask_login.current_user,
      comment = comment_form.comment.data,
      resto = resto
    )
    db.session.add(review)
    db.session.commit()

    return redirect(url_for('main.resto_detail', resto_id=resto_id))

  if form.validate_on_submit():
    resto.name = form.name.data
    resto.address = form.address.data
    resto.category = form.category.data
    db.session.add(resto)
    db.session.commit()

    flash('Resto updated!')
    return redirect(url_for('main.resto_detail', resto_id=resto_id))
  
  return render_template('resto_detail.html', resto=resto, comment_form=comment_form, form=form)
