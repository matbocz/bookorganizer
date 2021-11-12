from flask import render_template, request, url_for, redirect, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import send_email
from ..models import User


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        # Refresh authenticated user last seen date
        current_user.ping()

        # Redirect not confirmed user to unconfirmed_user page
        if not current_user.confirmed \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed_user'))


@auth.route('/unconfirmed_user')
def unconfirmed_user():
    # Redirect anonymous and confirmed users to main page
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))

    return render_template('auth/unconfirmed_user.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user=user, remember=form.remember_me.data)

            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('main.index')

            return redirect(next_url)

        flash('Invalid username or password.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    flash('You have been logged out.')

    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add new user to database
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # Send confirmation email to new user
        token = user.generate_user_confirm_token()
        send_email(to=user.email, subject="Confirm account", template='auth/mail/confirm_user', user=user, token=token)

        # Send email informing about new user to administrator
        app = current_app._get_current_object()
        if app.config['BOOKORGANIZER_ADMIN']:
            send_email(to=app.config['BOOKORGANIZER_ADMIN'], subject='New user', template='mail/new_user', user=user)

        # Show message on page
        flash('You can log in now.')

        # Redirect to main page
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form)


@auth.route('/confirm_user/<token>')
@login_required
def confirm_user(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_user(token):
        db.session.commit()
        flash('You have confirmed your account.')
    else:
        flash('Link is invalid or has expired.')

    return redirect(url_for('main.index'))
