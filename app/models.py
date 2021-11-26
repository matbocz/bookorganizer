import os
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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
    file = db.Column(db.Text())
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationships
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_file(self, file, type):
        """
        Save file to disk and save filename to database.

        :param file: This should be FileStorage
        :param type: This should be book or cover
        """
        file_types = ['book', 'cover']
        if type not in file_types:
            raise ValueError(f'Invalid file type. Expected one of: {file_types}')

        # Get current app and create secure filename
        app = current_app._get_current_object()
        filename = secure_filename(f'{self.id}_{type}_{file.filename}')

        # Check file type
        if type == 'book':
            # Remove old file from disk
            self.remove_file(type='book')

            # Save file to disk and save filename to database
            file.save(os.path.join(staticdir, app.config['UPLOADS_FOLDER'],
                                   app.config['BOOK_UPLOADS_FOLDER'], filename))
            self.file = filename
        if type == 'cover':
            # Remove old file from disk
            self.remove_file(type='cover')

            # Save file to disk and save filename to database
            file.save(os.path.join(staticdir, app.config['UPLOADS_FOLDER'],
                                   app.config['COVER_UPLOADS_FOLDER'], filename))
            self.cover = filename

    def remove_file(self, type):
        """
        Remove file from disk and remove filename from database.

        :param type: This should be book or cover
        """
        file_types = ['book', 'cover']
        if type not in file_types:
            raise ValueError(f'Invalid file type. Expected one of: {file_types}')

        # Get current app
        app = current_app._get_current_object()

        try:
            # Check file type
            if type == 'book':
                # Remove file from disk and remove filename from database
                os.remove(
                    os.path.join(staticdir, app.config['UPLOADS_FOLDER'],
                                 app.config['BOOK_UPLOADS_FOLDER'], self.file))
                self.file = None
            if type == 'cover':
                # Remove file from disk and remove filename from database
                os.remove(
                    os.path.join(staticdir, app.config['UPLOADS_FOLDER'],
                                 app.config['COVER_UPLOADS_FOLDER'], self.cover))
                self.cover = None
        except:
            pass

    def get_cover_file_url(self):
        """Return url to cover file."""
        app = current_app._get_current_object()

        return '/'.join([app.config['UPLOADS_FOLDER'], app.config['COVER_UPLOADS_FOLDER'], self.cover])

    def get_book_file_info(self):
        """Return book file info."""
        app = current_app._get_current_object()

        filename = os.path.splitext(self.file.split('_', 2)[2])[0]
        file_ext = os.path.splitext(self.file)[1]
        file_path = '/'.join([staticdir, app.config['UPLOADS_FOLDER'], app.config['BOOK_UPLOADS_FOLDER'], self.file])
        file_size_mb = os.stat(file_path).st_size / 1048576

        return {'name': filename, 'ext': file_ext, 'size': round(file_size_mb, 2)}

    def ping(self):
        """Refresh book date_modified column."""
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
    confirmed = db.Column(db.Boolean, default=False)

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

    # Generate token (Confirm User)
    def generate_user_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)

        return s.dumps({'confirm': self.id}).decode('utf-8')

    # Confirm User (token)
    def confirm_user(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)

        return True

    # Generate token (Reset Password)
    def generate_password_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)

        return s.dumps({'reset': self.id}).decode('utf-8')

    # Reset Password (token)
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])

        # Try to load token
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        # Get user from database and check if user exists
        user = User.query.get(data.get('reset'))
        if user is None:
            return False

        # Change user password
        user.password = new_password
        db.session.add(user)

        return True

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
