from flask import render_template, session, redirect, url_for, current_app, flash

from . import main
from .forms import NameForm
from .. import db
from ..email import send_email
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            if current_app.config['BOOKORGANIZER_ADMIN']:
                send_email(to=current_app.config['BOOKORGANIZER_ADMIN'],
                           subject='New User',
                           template='mail/new_user',
                           user=user)
            flash("You created a new user!")
            session['known'] = False
        else:
            flash("You logged in!")
            session['known'] = True

        session['name'] = form.name.data

        return redirect(url_for('.index'))

    return render_template('index.html',
                           form=form, name=session.get('name'), known=session.get('known', False))


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)
