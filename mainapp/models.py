from mainapp import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False )
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='dflt.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    likes = db.relationship('Likes', backref='liker', lazy=True)
    comments = db.relationship('Comment', backref='commentor', lazy=True)
    friends = db.relationship('Friends', backref='root_friend', lazy=True)
    lists = db.relationship('List', backref='lists', lazy=True)
    


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.friend_id}')"



class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.user_id}', '{self.post_id}')"


class Dislikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.user_id}')"



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.relationship('User', backref='author', lazy=True)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"



class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('Post', backref='tasks', lazy=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    privacy = db.Column(db.Boolean, nullable=False)
    def __repr__(self):
        return f"List('{self.name}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_due = db.Column(db.DateTime, nullable=True)
    list = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    comments = db.relationship('Comment', backref='comments', lazy=True)
    likes = db.Column(db.Integer, nullable=False, default=0)
    private = db.Column(db.Boolean, nullable=False)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
