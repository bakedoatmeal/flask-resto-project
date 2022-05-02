from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.main.forms import RestoForm
from app.models import Resto, User, MenuItem
from app.extensions import app, db

main = Blueprint('main', __name__)

# Create your routes here.
@main.route('/')
def index():
  restos = Resto.query.all()
  return render_template('home.html', restos = restos)

@main.route('/new_resto', methods=['GET', 'POST'])
def new_resto():
  form = RestoForm()

  if form.validate_on_submit():
    resto = Resto(
      name = form.name.data,
      address = form.address.data
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

  if form.validate_on_submit():
    resto = Resto(
      name = form.name.data,
      address = form.address.data
    )
    db.session.add(resto)
    db.session.commit()

    flash('Resto updated!')
    return redirect(url_for('main.resto_detail', resto_id=resto_id))
  
  return render_template('resto_detail.html', resto=resto, form=form)
