from faker import Faker
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User


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
                 member_since=fake.past_date())
        db.session.add(u)

        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
