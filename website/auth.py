from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Username or Password!', category='error')
        else:
            flash('Incorrect Username or Password!', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        passwordconf = request.form.get('passwordconf')

        checkemail = User.query.filter_by(email=email).first()
        checkname = User.query.filter_by(username=username).first()
        if checkemail:
            flash('Account already made with that email!', category='error')
        elif checkname:
            flash('Username taken!', category='error')
        elif not email.__contains__('@'):
            flash('Invalid email!', category='error')
        elif len(username) < 2:
            flash('Username must be longer than two characters!', category='error')
        elif password != passwordconf:
            flash('Passwords don\'t Match!', category='error')
        elif len(password) < 6:
            flash('Password must be at least six characters', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
