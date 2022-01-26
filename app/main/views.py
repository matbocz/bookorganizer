import os.path

from flask import render_template, flash, url_for, request, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from config import staticdir
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, AddBookForm, EditBookForm, SearchBookForm
from .. import db
from ..decorators import admin_required
from ..models import User, Role, Book


@main.route('/', methods=['GET', 'POST'])
def index():
    # Get URL parameters
    page = request.args.get(key='page', default=1, type=int)
    search = request.args.get(key='search', default="", type=str)

    # Handle SearchBookForm
    form = SearchBookForm()
    if form.is_submitted():
        search = form.title.data

        return redirect(url_for('main.index', search=search))

    # Get books from database
    pagination = Book.query.filter(Book.title.like(f'%{search}%')) \
        .order_by(Book.date_modified.desc()) \
        .paginate(page=page, per_page=current_app.config['BOOKS_PER_PAGE'], error_out=False)
    books = pagination.items

    # Render index page
    return render_template('index.html', pagination=pagination, books=books, search=search, form=form)


@main.route('/user/<username>')
def user(username):
    # Get URL parameters
    page = request.args.get(key='page', default=1, type=int)
    search = request.args.get(key='search', default="", type=str)

    # Get user from database
    user = User.query.filter_by(username=username).first_or_404()

    # Get books from database
    pagination = Book.query.filter(Book.title.like(f'%{search}%'), Book.owner_id == user.id) \
        .order_by(Book.date_modified.desc()) \
        .paginate(page=page, per_page=current_app.config['BOOKS_PER_PAGE'], error_out=False)
    books = pagination.items

    # Render user page
    return render_template('user.html', user=user, pagination=pagination, books=books, search=search)


@main.route('/book/<int:id>')
def book(id):
    book = Book.query.get_or_404(id)

    return render_template('book.html', book=book)


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
        flash(f'Book {book.title} has been added.')

        # Redirect to current user page
        return redirect(url_for('.user', username=current_user.username))

    # Render Add Book page
    return render_template('add_book.html', form=form)


@main.route('/delete-book/<int:id>')
@login_required
def delete_book(id):
    # Get selected book from database
    book = Book.query.get_or_404(id)

    # Check if current user is owner of selected book
    if current_user.is_owner(book):
        # Delete selected book file and cover
        book.remove_file(type='book')
        book.remove_file(type='cover')

        # Delete selected book from database
        db.session.delete(book)
        db.session.commit()

        # Show message on page
        flash(f'Book {book.title} has been deleted.')

        # Redirect to current user page
        return redirect(url_for('.user', username=current_user.username))

    # Show message on page
    flash(f'Book {book.title} cannot be deleted by you.')

    # Redirect to selected book page
    return redirect(url_for('.book', id=id))


@main.route('/edit-book/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)

    # Check if current user is owner of selected book
    if current_user.is_owner(book):
        form = EditBookForm()
        if form.validate_on_submit():
            # Update selected book data
            book.title = form.title.data
            book.author = form.author.data
            book.description = form.description.data

            # Update selected book cover
            if form.cover.data:
                cover = form.cover.data
                book.save_file(cover, type='cover')

            # Update selected book file
            if form.file.data:
                file = form.file.data
                book.save_file(file, type='book')

            # Send selected book data to database
            db.session.add(book)
            db.session.commit()

            # Show message on page
            flash('This book has been updated.')

            # Refresh selected book modified date
            book.ping()

            # Redirect to selected book page
            return redirect(url_for('.book', id=id))

        # Fill out form with selected book data
        form.title.data = book.title
        form.author.data = book.author
        form.description.data = book.description

        # Render Edit Book page
        return render_template('edit_book.html', form=form)

    # Show message on page
    flash('This book cannot be updated by you.')

    # Redirect to selected book page
    return redirect(url_for('.book', id=id))


@main.route('/download/<filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    """Download book file from server."""
    app = current_app._get_current_object()

    # Get selected book from database
    book = Book.query.filter_by(file=filename).first_or_404()

    # Check if current user is owner of selected book
    if current_user.is_owner(book):
        # Create path to selected book file
        path = os.path.join(staticdir, app.config['UPLOADS_FOLDER'], app.config['BOOK_UPLOADS_FOLDER'], filename)

        # Create download name for book file
        download_name = filename.split('_', 2)[2]

        # Send file to client
        return send_file(path, as_attachment=True, download_name=download_name)

    # Show message on page
    flash('This book cannot be downloaded by you.')

    # Redirect to selected book page
    return redirect(url_for('.book', id=book.id))


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
