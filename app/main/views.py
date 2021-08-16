from flask import render_template, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from . import main
from .forms import EditProfileForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Update current user data
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data

        # Send current user data to database
        db.session.add(current_user._get_current_object())
        db.session.commit()

        # Show message on page
        flash('Your profile has been updated.')

        # Redirect to current user page
        return redirect(url_for('.user', username=current_user.username))

    # Fill out form with current user data
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me

    # Render Edit Profile page
    return render_template('edit_profile.html', form=form)
