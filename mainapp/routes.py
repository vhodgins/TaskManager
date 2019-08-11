#package folder, database classes
from mainapp.models import User, Post, Comment
#flask functions
from flask import escape, render_template, request, url_for, flash, redirect, abort, jsonify
#package folder, Forms
from mainapp.forms import Check, RegisterForm, LoginForm, UpdateForm, CreateTask, CommentForm
#flesk app, SQLAlchemy database, bcyrpt password hash
from mainapp import app, db, bcrypt
#login session
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
import time
from datetime import datetime


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'Hello'
    localtimes = []
    if current_user.is_authenticated:
        title = "Hello  " + str(current_user.username)
        tasks=Post.query.filter(Post.user_id != current_user.id).all()
    else:
        tasks = []

    if tasks:
        for task in tasks:
            localtimes.append(datetime_from_utc_to_local(task.date_posted))
    comment = CommentForm()
    form = CreateTask()


    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash(f'You must be logged in to do that')
            return redirect(url_for('home'))
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('home.html', title=title, tasks=tasks, form=form,comment=comment, localtimes=localtimes)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged In', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Woops, incorrect email or password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/weight')
def weight():
    return render_template('weight.html',title='Weight')

def save_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pfps', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/posts/<post_id>', methods=['GET','POST'])
@login_required
def post(post_id):
    form = CreateTask()
    post = Post.query.get_or_404(post_id)
    localtime=datetime_from_utc_to_local(post.date_posted)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content= form.content.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post.html', form=form, task=post, title=post.title, localtime=localtime)


@app.route('/posts/<post_id>/update')
@login_required
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreateTask()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash(f'You must be logged in to do that')
            return redirect(url_for('home'))
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('update.html', form=form, task=post, title="Update Post")




@app.route('/check_task', methods=['GET','POST'])
def check_task():
    task = Post.query.filter_by(id=request.form['id']).first()
    if task.content != 'Completed':
        task.content = 'Completed'
        db.session.commit()
        return jsonify({'result' : 'success', 'Content' : 'Completed', 'button_img' :url_for('static', filename='assets/x.png')})
    else:
        task.content = ''
        db.session.commit()
        return jsonify({'result' : 'success', 'Content' : '', 'button_img' : url_for('static', filename='assets/check.png') })




@app.route('/account/<account_id>', methods=['GET','POST'])
@login_required
def account(account_id):
    account = User.query.get_or_404(account_id)
    form = UpdateForm()
    tasks=Post.query.filter_by(user_id=account.id).all()
    localtimes = []
    if tasks:
        for task in tasks:
            localtimes.append(datetime_from_utc_to_local(task.date_posted))
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"your account was updated", 'success')
        return redirect(url_for('account', account_id=current_user.id))
    elif request.method == 'GET':
        form.username.data = account.username
        form.email.data = account.email
    image_file = url_for('static', filename='pfps/'+current_user.image_file)
    return render_template('account.html', title=account.username+"'s tasks", image_file=image_file, account=account, localtimes=localtimes, form=form, tasks=tasks)
