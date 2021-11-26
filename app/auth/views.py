from flask import render_template, request, url_for, redirect, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm
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

        # Redirect to login page
        return redirect(url_for('auth.login'))

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


@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    # Redirect anonymous and confirmed users to main page
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))

    # Resend confirmation email to new user
    token = current_user.generate_user_confirm_token()
    send_email(to=current_user.email, subject="Confirm account", template='auth/mail/confirm_user', user=current_user,
               token=token)

    # Show message on page
    flash(f'A new account confirmation link has been sent to the e-mail address: {current_user.email}.')

    # Redirect to unconfirmed page
    return redirect(url_for('auth.unconfirmed_user'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            # Change user password
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()

            # Show message on page
            flash("You have changed your password.")

            # Redirect to main page
            return redirect(url_for("main.index"))
        else:
            # Show message on page
            flash("Invalid old password.")

    # Render change_password template
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    # Redirect all users to main page (except anonymous users)
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))

    # Check if form has been submitted
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # Get user from database
        user = User.query.filter_by(email=form.email.data.lower()).first()

        # Check if user exists
        if user:
            # Generate token and send e-mail with this token
            token = user.generate_password_reset_token()
            send_email(to=user.email, subject="Reset password", template='auth/mail/reset_password', user=user,
                       token=token)

            # Show message on page
            flash(f'A reset password link has been sent to the e-mail address: {user.email}.')

            # Redirect to login page
            return redirect(url_for('auth.login'))

    # Render reset_password_request template
    return render_template('auth/reset_password_request.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Redirect all users to main page (except anonymous users)
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))

    # Check if form has been submitted
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Check if password has been reset correctly
        if User.reset_password(token, form.new_password.data):
            # Commit database changes
            db.session.commit()

            # Show message on page
            flash("You have reset your password.")

            # Redirect to login page
            return redirect(url_for('auth.login'))
        else:
            # Redirect to main page
            return redirect(url_for('main.index'))

    # Render reset_password template
    return render_template('auth/reset_password.html', form=form)
