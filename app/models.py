from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager


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

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # Relationships
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
