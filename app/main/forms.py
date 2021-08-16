from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length


class EditProfileForm(FlaskForm):
    name = StringField('Name',
                       validators=[Length(min=0, max=64,
                                          message='Name must be between 0 and 64 characters long.')])
    location = StringField('Location',
                           validators=[Length(min=0, max=64,
                                              message='Location must be between 0 and 64 characters long.')])
    about_me = TextAreaField('About me')

    submit = SubmitField('Save changes')
