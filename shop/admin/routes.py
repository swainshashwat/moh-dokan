import email
from argon2 import hash_password
from flask import render_template, session, request, redirect, url_for, flash
from matplotlib.pyplot import title
from numpy import prod

from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
import os

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html',
     title='Admin Page', products=products)

@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html',
     title='Brand page', brands=brands)

@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html',
     title='Category page', categories=categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Welcome {form.name.data}! Thanks for registering', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form, title="Registration page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}. You are logged in now!', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password please try again', 'danger')


    return render_template('admin/login.html', form=form, tutle='Login Page')