from flask import Flask, render_template, redirect, url_for, request, session, flash, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, FileField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, URL
import os
import datetime
import uuid
from flask_migrate import Migrate
import vobject

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secret key of your choice
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'static/res/profile_image/'

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Add this line

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    facebook = db.Column(db.String(100), nullable=False)
    instagram = db.Column(db.String(100), nullable=False)
    linkedin = db.Column(db.String(100), nullable=False)
    twitter = db.Column(db.String(100), nullable=False)
    profile_image_url = db.Column(db.String(200), nullable=True)
    show_services = db.Column(db.Boolean, default=False)
    service1_title = db.Column(db.String(100), nullable=True)
    service1_description = db.Column(db.Text, nullable=True)
    service2_title = db.Column(db.String(100), nullable=True)
    service2_description = db.Column(db.Text, nullable=True)
    service3_title = db.Column(db.String(100), nullable=True)
    service3_description = db.Column(db.Text, nullable=True)
    service4_title = db.Column(db.String(100), nullable=True)
    service4_description = db.Column(db.Text, nullable=True)
    editor_username = db.Column(db.String(100), unique=True, nullable=True)
    editor_password = db.Column(db.String(100), nullable=True)

# Define the User form
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
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

class EditorLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Sample users for demonstration purposes
users = {
    'admin': 'password',
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'username' in session:
        users = User.query.order_by(User.id.desc()).limit(10).all()  # Show recent 10 users
        return render_template('admin.html', username=session['username'], users=users)
    else:
        flash('You need to be logged in to view the admin page')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session:
        flash('You need to be logged in to add a user')
        return redirect(url_for('login'))

    form = UserForm()
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('The username is already in use.')
            return redirect(url_for('add_user'))

        profile_image = form.profile_image_url.data
        profile_image_path = None
        if profile_image:
            # Generate a unique filename
            unique_filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + os.path.splitext(profile_image.filename)[1]
            profile_image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            profile_image.save(profile_image_path)
            profile_image_path = unique_filename

        new_user = User(
            username=form.username.data,
            name=form.name.data,
            designation=form.designation.data,
            about=form.about.data,
            phone=form.phone.data,
            email=form.email.data,
            website=form.website.data,
            location=form.location.data,
            facebook=form.facebook.data,
            instagram=form.instagram.data,
            linkedin=form.linkedin.data,
            twitter=form.twitter.data,
            profile_image_url=profile_image_path,
            show_services=form.show_services.data,
            service1_title=form.service1_title.data,
            service1_description=form.service1_description.data,
            service2_title=form.service2_title.data,
            service2_description=form.service2_description.data,
            service3_title=form.service3_title.data,
            service3_description=form.service3_description.data,
            service4_title=form.service4_title.data,
            service4_description=form.service4_description.data,
            editor_username=form.phone.data,  # Using phone as username
            editor_password=str(uuid.uuid4())  # Generating a unique password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('admin'))

    return render_template('add_user.html', form=form)

@app.route('/edit/<string:user_uuid>', methods=['GET', 'POST'])
def edit_user(user_uuid):
    if 'editor' in session and session['editor']['uuid'] == user_uuid:
        user = User.query.filter_by(uuid=user_uuid).first_or_404()
        form = UserForm(obj=user)
        if form.validate_on_submit():
            # Update user attributes from the form
            user.username = form.username.data
            user.name = form.name.data
            user.designation = form.designation.data
            user.about = form.about.data
            user.phone = form.phone.data
            user.email = form.email.data
            user.website = form.website.data
            user.location = form.location.data
            user.facebook = form.facebook.data
            user.instagram = form.instagram.data
            user.linkedin = form.linkedin.data
            user.twitter = form.twitter.data
            user.show_services = form.show_services.data
            user.service1_title = form.service1_title.data
            user.service1_description = form.service1_description.data
            user.service2_title = form.service2_title.data
            user.service2_description = form.service2_description.data
            user.service3_title = form.service3_title.data
            user.service3_description = form.service3_description.data
            user.service4_title = form.service4_title.data
            user.service4_description = form.service4_description.data
            
            # Handle the profile image update only if a new image is provided
            profile_image = form.profile_image_url.data
            if profile_image:
                # Generate a unique filename
                unique_filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + os.path.splitext(profile_image.filename)[1]
                profile_image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                profile_image.save(profile_image_path)
                user.profile_image_url = unique_filename

            db.session.commit()
            flash('User updated successfully!')
            return redirect(url_for('user_detail', username=user.username))
        return render_template('edit_user.html', form=form, user=user)
    else:
        return redirect(url_for('editor_login', user_uuid=user_uuid))

@app.route('/editor_login/<string:user_uuid>', methods=['GET', 'POST'])
def editor_login(user_uuid):
    form = EditorLoginForm()
    user = User.query.filter_by(uuid=user_uuid).first_or_404()
    
    if form.validate_on_submit():
        if user.editor_username == form.username.data and user.editor_password == form.password.data:
            session['editor'] = {'uuid': user_uuid}
            return redirect(url_for('edit_user', user_uuid=user_uuid))
        else:
            flash('Invalid credentials')
    
    return render_template('editor_login.html', form=form, user=user, user_uuid=user_uuid)

@app.route('/user/<username>')
def user_detail(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_detail.html', user=user)

@app.route('/download_vcf/<username>')
def download_vcf(username):
    user = User.query.filter_by(username=username).first_or_404()

    vcard = vobject.vCard()
    vcard.add('fn').value = user.name
    vcard.add('tel').value = user.phone
    vcard.add('email').value = user.email

    output = vcard.serialize()
    
    response = make_response(output)
    response.headers["Content-Disposition"] = f"attachment; filename={user.username}.vcf"
    response.headers["Content-Type"] = "text/vcard"
    return response

@app.route('/check_username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    return jsonify({'available': user is None})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
