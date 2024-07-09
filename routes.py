from flask import render_template, redirect, url_for, request, session, flash
from . import db
from .models import User
from .forms import UserForm
import os
from . import create_app

app = create_app()

# Sample user for demonstration purposes
users = {'admin': 'password'}

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
        return render_template('admin.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session:
        return redirect(url_for('login'))

    form = UserForm()
    if form.validate_on_submit():
        profile_image = form.profile_image_url.data
        if profile_image:
            profile_image_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_image.filename)
            profile_image.save(profile_image_path)
        else:
            profile_image_path = None

        new_user = User(
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
            service4_description=form.service4_description.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('admin'))

    return render_template('add_user.html', form=form)
