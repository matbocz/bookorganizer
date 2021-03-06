from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(message='Email is required.'),
                                    Length(min=3, max=64,
                                           message='Email must be between 3 and 64 characters long.'),
                                    Email(message='Email must be valid.')])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Password is required.'),
                                         Length(min=10, max=64,
                                                message='Password must be between 10 and 64 characters long.')])
    remember_me = BooleanField('Remember me')


class RegistrationForm(FlaskForm):
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

    password = PasswordField('Password',
                             validators=[DataRequired(message='Password is required.'),
                                         Length(min=10, max=64,
                                                message='Password must be between 10 and 64 characters long.')])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(message='Password confirmation is required.'),
                                          EqualTo(fieldname='password',
                                                  message='Passwords must be identical.')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password',
                                 validators=[DataRequired(message='Old password is required.')])

    new_password = PasswordField('New password',
                                 validators=[DataRequired(message='New password is required.'),
                                             Length(min=10, max=64,
                                                    message='New password must be between 10 and 64 characters long.')])
    new_password2 = PasswordField('Confirm new password',
                                  validators=[DataRequired(message='New password confirmation is required.'),
                                              EqualTo(fieldname='new_password',
                                                      message='New passwords must be identical.')])


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(message='Email is required.'),
                                    Length(min=3, max=64,
                                           message='Email must be between 3 and 64 characters long.'),
                                    Email(message='Email must be valid.')])


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New password',
                                 validators=[DataRequired(message='New password is required.'),
                                             Length(min=10, max=64,
                                                    message='New password must be between 10 and 64 characters long.')])
    new_password2 = PasswordField('Confirm new password',
                                  validators=[DataRequired(message='New password confirmation is required.'),
                                              EqualTo(fieldname='new_password',
                                                      message='New passwords must be identical.')])


class ChangeEmailForm(FlaskForm):
    new_email = StringField('New e-mail',
                            validators=[DataRequired(message='New e-mail is required.'),
                                        Length(min=3, max=64,
                                               message='New e-mail must be between 3 and 64 characters long.'),
                                        Email(message='New e-mail must be valid.')])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Password is required.'),
                                         Length(min=10, max=64,
                                                message='Password must be between 10 and 64 characters long.')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail is already in use.')
