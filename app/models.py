import os
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import staticdir
from . import db
from . import login_manager


class Book(db.Model):
    __tablename__ = 'books'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    author = db.Column(db.String(64))
    description = db.Column(db.Text())
    cover = db.Column(db.Text())
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationships
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_cover(self, cover):
        """Save cover to file and cover name to database."""
        app = current_app._get_current_object()
        filename = secure_filename(f'{self.id}_{cover.filename}')

        # Remove old cover file
        try:
            os.remove(
                os.path.join(staticdir, app.config['UPLOADS_FOLDER'], app.config['COVER_UPLOADS_FOLDER'], self.cover))
        except:
            pass

        # Save new cover file and new cover name to database
        cover.save(os.path.join(staticdir, app.config['UPLOADS_FOLDER'], app.config['COVER_UPLOADS_FOLDER'], filename))
        self.cover = filename

    def get_cover_file_url(self):
        """Return url to cover file."""
        app = current_app._get_current_object()

        return '/'.join([app.config['UPLOADS_FOLDER'], app.config['COVER_UPLOADS_FOLDER'], self.cover])

    # Refresh Book modified date
    def ping(self):
        self.date_modified = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Book %r>' % self.title


class Role(db.Model):
    __tablename__ = 'roles'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    # Relationships
    users = db.relationship('User', backref='role', lazy='dynamic')

    # Add permission to Role
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    # Remove permission from Role
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    # Reset Role permissions
    def reset_permissions(self):
        self.permissions = 0

    # Check Role permission
    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.Organize],
            'Administrator': [Permission.Organize, Permission.Admin],
        }
        default_role = 'User'

        for role_name in roles:
            # Look for role in database
            role = Role.query.filter_by(name=role_name).first()

            # Create role if not in database
            if role is None:
                role = Role(name=role_name)

            # Reset role permissions
            role.reset_permissions()

            # Add permissions to role
            for perm in roles[role_name]:
                role.add_permission(perm)

            # Set default role
            role.default = (role.name == default_role)

            db.session.add(role)
        db.session.commit()

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name


class Permission:
    Organize = 1
    Admin = 2


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationships
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    books = db.relationship('Book', backref='owner', lazy='dynamic')

    # Password getter
    @property
    def password(self):
        raise AttributeError('Unable to read password.')

    # Password setter
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Password verification
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Check User permission
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    # Check if User is administrator
    def is_administrator(self):
        return self.can(Permission.Admin)

    # Check if User is owner of specific Book
    def is_owner(self, book):
        for item in self.books.all():
            if item.id == book.id:
                return True

        return False

    # Refresh User last seen date
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if self.role is None:
            if self.email == current_app.config['BOOKORGANIZER_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    # Check AnonymousUser permission
    def can(self, perm):
        return False

    # Check if AnonymousUser is administrator
    def is_administrator(self):
        return False

    # Check if AnonymousUser is owner of specific Book
    def is_owner(self, book):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
