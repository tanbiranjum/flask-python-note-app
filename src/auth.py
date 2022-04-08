from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def Login():
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You have successfully logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.Home'))
            else:
                flash('Incorrent password', category='danger')
        else:
            flash('No user found', category='danger')

    return render_template("login.html", user=current_user)


@auth.route('/register', methods=['GET', 'POST'])
def Register():
    if(request.method == 'POST'):
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        passwordConfirm = request.form['password-confirm']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='danger')
        elif len(email) < 4:
            flash("Email must be at least 4 characters long", category="error")
        elif(len(name) < 4):
            flash("Name must be at least 4 characters long", category="error")
        elif(len(password) < 4):
            flash("Password must be at least 4 characters long", category="error")
        elif(password != passwordConfirm):
            flash("Passwords do not match", category="error")
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Success", category="success")
            login_user(user, remember=true)
            return redirect(url_for('views.Home'))

    return render_template("register.html", user=current_user)


@auth.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('auth.Login'))
