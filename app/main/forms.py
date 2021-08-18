from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, DataRequired, Email, Regexp, ValidationError

from app.models import Role, User


class AddBookForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(message='Title is required.'),
                                    Length(min=1, max=64,
                                           message='Title must be between 1 and 64 characters long.')])
    author = StringField('Author',
                         validators=[Length(min=0, max=64,
                                            message='Author must be between 0 and 64 characters long.')])
    description = TextAreaField('Description')

    submit = SubmitField('Add book')


class EditProfileForm(FlaskForm):
    name = StringField('Name',
                       validators=[Length(min=0, max=64,
                                          message='Name must be between 0 and 64 characters long.')])
    location = StringField('Location',
                           validators=[Length(min=0, max=64,
                                              message='Location must be between 0 and 64 characters long.')])
    about_me = TextAreaField('About me')

    submit = SubmitField('Save changes')


class EditProfileAdminForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(message='Email is required.'),
                                    Length(min=3, max=64,
                                           message='Email must be between 3 and 64 characters long.'),
                                    Email(message='Email must be valid.')])
    username = StringField('Username',
                           validators=[DataRequired(message='Username is required.'),
                                       Length(min=3, max=64,
                                              message='Username must be between 3 and 64 characters long.'),
                                       Regexp(regex='^[A-Za-z][A-Za-z0-9_]*$',
                                              flags=0,
                                              message='Username must start with a letter '
                                                      'and can only contain letters, numbers and underscores.')])
    role = SelectField('Role',
                       coerce=int)
    name = StringField('Name',
                       validators=[Length(min=0, max=64,
                                          message='Name must be between 0 and 64 characters long.')])
    location = StringField('Location',
                           validators=[Length(min=0, max=64,
                                              message='Location must be between 0 and 64 characters long.')])
    about_me = TextAreaField('About me')

    submit = SubmitField('Save changes')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)

        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail is already in use.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already in use.')
