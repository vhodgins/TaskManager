#package folder, database classes
from mainapp.models import *
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
import re


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


@app.route('/', methods=['GET', 'POST'])
#@login_required
def home():




    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    title = 'Hello'
    localtimes = {}
    mytasklocaltimes = {}

    if current_user.is_authenticated:
        if not List.query.filter_by(user =current_user.id).all():
            l = List(name='To-do', user=current_user.id, privacy=False)
            db.session.add(l)
            db.session.commit()
        title = 'Wacky Schemes'
        tasks=Post.query.filter(Post.user_id != current_user.id).all()
        mytasks = Post.query.filter_by(user_id=current_user.id).all()
    else:
        tasks = []
        mytasks=[]

    tasklikes = {}

    if tasks:
        for task in tasks:
            #likelist = Likes.query.filter(Likes.post_id==task.id).all()
            likecount = len(Likes.query.filter_by(post_id=task.id).all()) - len(Dislikes.query.filter_by(post_id=task.id).all())
            tasklikes.update({task.id : likecount})
            localtimes.update({task.id : datetime_from_utc_to_local(task.date_posted)})
    if mytasks:
        for task in mytasks:
            likecount = len(Likes.query.filter_by(post_id=task.id).all()) - len(Dislikes.query.filter_by(post_id=task.id).all())
            tasklikes.update({task.id : likecount})
            mytasklocaltimes.update({task.id : datetime_from_utc_to_local(task.date_posted) })

    comment = CommentForm()
    form = CreateTask()

    likes = {}
    if tasks:
        for task in tasks:
            if Likes.query.filter(Likes.user_id==current_user.id).filter(Likes.post_id==task.id).first():
                likes.update({task.id : 1})
            elif Dislikes.query.filter(Dislikes.user_id==current_user.id).filter(Dislikes.post_id==task.id).first():
                likes.update({task.id :-1})
            else:
                likes.update({task.id : 0})

    if mytasks:
        for task in mytasks:
            if Likes.query.filter(Likes.user_id==current_user.id).filter(Likes.post_id==task.id).first():
                likes.update({task.id : 1})
            elif Dislikes.query.filter(Dislikes.user_id==current_user.id).filter(Dislikes.post_id==task.id).first():
                likes.update({task.id :-1})
            else:
                likes.update({task.id : 0})

    lists = List.query.filter_by(user=current_user.id).all()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash(f'You must be logged in to do that')
            return redirect(url_for('home'))
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('home.html',lists=lists, home='home', tasklikes=tasklikes, title=title, likes=likes, account=current_user, tasks=tasks, mytasklocaltimes=mytasklocaltimes, mytasks=mytasks, form=form,comment=comment, localtimes=localtimes)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        #flash(f'Logged In', 'success')
        return redirect(next_page) if next_page else redirect(url_for('home'))
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='register', form=form)


@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if not current_user.is_authenticated:
        flash(f'You must be logged in to do that')
        return redirect(url_for('home'))
    title = request.form['title']
    list = request.form['list']
    date = request.form['date']
    private = True if request.form['private'] else False
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')
    else:
        date = datetime.strptime('1907', '%Y')
    post = Post(title=title, content='', user_id=current_user.id, list=list, date_due = date, private=private)

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/fetch_tasks', methods=['GET', 'POST'])
def fetch_tasks():
    list = request.form['list']
    tasks = List.query.filter_by(name=list, user=current_user.id).first().tasks
    return jsonify({'result' : 'success', 'tasks' : tasks})

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
            #flash(f'Logged In', 'success')
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
    likes = len(Likes.query.filter_by(post_id=post.id).all()) - len(Dislikes.query.filter_by(post_id=post.id).all())
    if form.validate_on_submit():
        post.title = form.title.data
        post.content= form.content.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post.html', form=form, likes=likes, account=current_user, task=post, title=post.title, localtime=localtime)



@app.route('/search/<field_query>', methods=['GET', 'POST'])
def search(field_query):
    accounts = User.query.filter(User.username.contains(str(field_query))).all()
    accounts = sorted(accounts, key=lambda user: user.username)
    if current_user.is_authenticated:
        friends = [friend.friend_id for friend in current_user.friends]
    else:
        friends = []
    return render_template('search.html', accounts = accounts, friends= friends)


@app.route('/upvote', methods=['GET','POST'])
def upvote():
    task = request.form['id']
    if request.form['lean'] == 'pos':
        if Dislikes.query.filter_by(user_id=current_user.id, post_id=task).first():
            db.session.delete(Dislikes.query.filter_by(user_id=current_user.id, post_id=task).first())
        db.session.add(Likes(user_id=current_user.id, post_id=task))
        db.session.commit()
    if request.form['lean'] == 'neg' :
        if Likes.query.filter_by(user_id=current_user.id, post_id=task).first():
            db.session.delete(Likes.query.filter_by(user_id=current_user.id, post_id=task).first())
        db.session.add(Dislikes(user_id=current_user.id, post_id=task))
        db.session.commit()
    if request.form['lean'] == 'neutral' :
        if Likes.query.filter_by(user_id=current_user.id, post_id=task).first():
            db.session.delete(Likes.query.filter_by(user_id=current_user.id, post_id=task).first())
        if Dislikes.query.filter_by(user_id=current_user.id, post_id=task).first():
            db.session.delete(Dislikes.query.filter_by(user_id=current_user.id, post_id=task).first())
        db.session.commit()

    likecount = len(Likes.query.filter_by(post_id=task).all()) - len(Dislikes.query.filter_by(post_id=task).all())
    return jsonify({'result' : 'success', 'likes' : likecount })

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

@app.route('/delete_list', methods=['GET', 'POST'])
def delete_list():
    id = request.form['id']
    list = List.query.filter_by(id=id).first()
    for task in list.tasks:
        for comment in task.comments:
            db.session.delete(comment)
        db.session.delete(task)
    db.session.commit()
    db.session.delete(list)
    db.session.commit()
    return jsonify({'result': 'success'})



@app.route('/check_task', methods=['GET','POST'])
def check_task():
    task = Post.query.filter_by(id=request.form['id']).first()
    if task.content != 'Completed':
        task.content = 'Completed'
        db.session.commit()
        return jsonify({'result' : 'success', 'Content' : 'Completed', 'button_img' :url_for('static', filename='assets/x.png')})
    '''else:
        task.content = ''
        db.session.commit()
        return jsonify({'result' : 'success', 'Content' : '', 'button_img' : url_for('static', filename='assets/check.png') })'''




@app.route('/account/<account_id>', methods=['GET','POST'])
@login_required
def account(account_id):
    title = 'Hello'
    localtimes = {}
    mytasklocaltimes = {}
    lists = List.query.filter_by(user=account_id).all()
    if current_user.is_authenticated:
        title = 'Wacky Schemes'
        tasks=Post.query.filter(Post.user_id != current_user.id).all()
        mytasks = Post.query.filter_by(user_id=current_user.id).all()
    else:
        tasks = []
        mytasks=[]
    tasklikes = {}
    if tasks:
        for task in tasks:
            #likelist = Likes.query.filter(Likes.post_id==task.id).all()
            likecount = len(Likes.query.filter_by(post_id=task.id).all()) - len(Dislikes.query.filter_by(post_id=task.id).all())
            tasklikes.update({task.id : likecount})
            localtimes.update({task.id : datetime_from_utc_to_local(task.date_posted)})
    if mytasks:
        for task in mytasks:
            likecount = len(Likes.query.filter_by(post_id=task.id).all()) - len(Dislikes.query.filter_by(post_id=task.id).all())
            tasklikes.update({task.id : likecount})
            localtimes.update({task.id : datetime_from_utc_to_local(task.date_posted)})
    likes = {}
    if tasks:
        for task in tasks:
            if Likes.query.filter(Likes.user_id==current_user.id).filter(Likes.post_id==task.id).first():
                likes.update({task.id : 1})
            elif Dislikes.query.filter(Dislikes.user_id==current_user.id).filter(Dislikes.post_id==task.id).first():
                likes.update({task.id :-1})
            else:
                likes.update({task.id : 0})
    if mytasks:
        for task in mytasks:
            if Likes.query.filter(Likes.user_id==current_user.id).filter(Likes.post_id==task.id).first():
                likes.update({task.id : 1})
            elif Dislikes.query.filter(Dislikes.user_id==current_user.id).filter(Dislikes.post_id==task.id).first():
                likes.update({task.id :-1})
            else:
                likes.update({task.id : 0})
    account = User.query.get_or_404(account_id)



    image_file = url_for('static', filename='pfps/'+current_user.image_file)
    return render_template('account.html', lists=lists, title=account.username+"'s tasks", page='account', localtimes = localtimes ,tasks=tasks, likes=likes, tasklikes=tasklikes, image_file=image_file, account=account, mytasklocaltimes=localtimes,  mytasks=tasks)

@app.route('/account/<account_id>/following', methods=['GET', 'POST'])
def following(account_id):
    account = User.query.filter_by(id=account_id).first()
    friends = {}
    for user in account.friends:
        u = int(user.friend_id)
        friends.update({u : User.query.filter_by(id=user.friend_id).first()})

    return render_template('following.html' , account=account, friends=friends)

@app.route('/account/<account_id>/followers', methods=['GET', 'POST'])
def followers(account_id):
    accounts = Friends.query.filter_by(user_id=account_id).all()
    followers = []
    for account in accounts:
        follower = User.query.filter_by(id=account.id).first()
        followers.append(follower)


    return render_template('followers.html' , followers=followers)

@app.route('/delete_post', methods=["GET", "POST"])
def delete_post():
    id = list(map(int, re.findall(r'\d+', request.form['id'])))[0]
    print(id)
    comments = Comment.query.filter_by(post=Post.query.filter_by(id=id).first().id).all()
    if comments:
        for comment in comments:
            db.session.delete(comment)
    db.session.commit()
    db.session.delete(Post.query.filter_by(id=id).first())
    db.session.commit()
    return jsonify({'result' : 'success'})



@app.route('/make_comment', methods=["GET", "POST"])
def make_comment():
    c = Comment(user_id=current_user.id, content=request.form['content'], post=request.form['post'])
    db.session.add(c)
    db.session.commit()
    return jsonify({'result' : 'success'})


@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    print(request.form['id'])
    print([friend.friend_id for friend in current_user.friends])
    if int(request.form['id']) in [friend.friend_id for friend in current_user.friends]:
            f = Friends.query.filter_by(user_id=current_user.id , friend_id = int(request.form['id'])).first()
            db.session.delete(f)
    else:
        f = Friends(user_id = current_user.id , friend_id = request.form['id'])

        db.session.add(f)
    db.session.commit()
    return jsonify({'result' : 'success'})

@app.route('/newlist', methods=['GET', 'POST'])
def newlist():
    name = request.form['name']
    private = request.form['private']
    if private == 'false':
        private = False
    else:
        private = True

    l = List(name=name, user=current_user.id, privacy=private)
    db.session.add(l)
    db.session.commit()
    return jsonify({'result' : 'success'})




@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    l = List.query.filter_by(user=current_user.id)
    return render_template('dashboard.html', lists = l)
