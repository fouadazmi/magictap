from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, URL

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    about = TextAreaField('About', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    website = StringField('Website', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    facebook = StringField('Facebook', validators=[URL()])
    instagram = StringField('Instagram', validators=[URL()])
    linkedin = StringField('LinkedIn', validators=[URL()])
    twitter = StringField('Twitter', validators=[URL()])
    profile_image_url = FileField('Profile Image')
    show_services = BooleanField('Show Services')
    service1_title = StringField('Service 1 Title')
    service1_description = TextAreaField('Service 1 Description')
    service2_title = StringField('Service 2 Title')
    service2_description = TextAreaField('Service 2 Description')
    service3_title = StringField('Service 3 Title')
    service3_description = TextAreaField('Service 3 Description')
    service4_title = StringField('Service 4 Title')
    service4_description = TextAreaField('Service 4 Description')
    submit = SubmitField('Submit')
