from random import randint

from faker import Faker
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User, Book


def users(count=10):
    fake = Faker()

    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='1234567890',
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date(),
                 confirmed=True)
        db.session.add(u)

        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def books(count=10):
    fake = Faker()

    user_count = User.query.count()
    for i in range(count):
        date = fake.past_date()
        u = User.query.offset(randint(0, user_count - 1)).first()

        b = Book(title=fake.word(),
                 author=fake.name(),
                 description=fake.text(),
                 date_added=date,
                 date_modified=date,
                 owner=u)
        db.session.add(b)

        db.session.commit()
