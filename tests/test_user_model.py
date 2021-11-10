import time
import unittest

from app import create_app, db
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='book')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='book')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='book')
        self.assertTrue(u.verify_password('book'))
        self.assertFalse(u.verify_password('movie'))

    def test_password_salts_are_random(self):
        u = User(password='book')
        u2 = User(password='book')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_user_confirm_token(self):
        u = User(password='book')
        db.session.add(u)
        db.session.commit()
        token = u.generate_user_confirm_token()
        self.assertTrue(u.confirm_user(token))

    def test_invalid_user_confirm_token(self):
        u1 = User(password='book')
        u2 = User(password='movie')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_user_confirm_token()
        self.assertFalse(u2.confirm_user(token))

    def test_expired_user_confirm_token(self):
        u = User(password='book')
        db.session.add(u)
        db.session.commit()
        token = u.generate_user_confirm_token(expiration=1)
        time.sleep(2)
        self.assertFalse(u.confirm_user(token))

    def test_user_role(self):
        u = User(email='user@email.com', password='book')
        self.assertTrue(u.can(Permission.Organize))
        self.assertFalse(u.can(Permission.Admin))

    def test_administrator_role(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='user@email.com', password='book', role=r)
        self.assertTrue(u.can(Permission.Organize))
        self.assertTrue(u.can(Permission.Admin))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.Organize))
        self.assertFalse(u.can(Permission.Admin))
