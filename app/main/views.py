from flask import render_template, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from . import main
from .forms import EditProfileForm, EditProfileAdminForm, AddBookForm
from .. import db
from ..decorators import admin_required
from ..models import User, Role, Book


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)


@main.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        # Create book object
        book = Book(title=form.title.data,
                    author=form.author.data,
                    description=form.description.data,
                    owner=current_user._get_current_object())

        # Send book object to database
        db.session.add(book)
        db.session.commit()

        # Show message on page
        flash('Book has been added.')

        # Redirect to current user page
        return redirect(url_for('.user', username=current_user.username))

    # Render Add Book page
    return render_template('add_book.html', form=form)


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


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)

    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        # Update selected user data
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data

        # Send selected user data to database
        db.session.add(user)
        db.session.commit()

        # Show message on page
        flash('Profile has been updated.')

        # Redirect to selected user page
        return redirect(url_for('.user', username=user.username))

    # Fill out form with selected user data
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me

    # Render Edit Profile [Admin] page
    return render_template('edit_profile_admin.html', form=form)
