from crypt import methods
from flask import Flask, render_template, redirect, flash, abort, request
from forms import RegistrationForm, LoginForm, UpdateForm
from flask_login import login_user, logout_user, current_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = 'OurSuperSecretKey'

from models import db, User, Post

context = [
    {
        'title': 'Blog 1',
        'content': 'This is the content of the first blog',
        'author' : 'Kapil',
        'date' : '10/10/2021'
    },
    {
        'title': 'Blog 2',
        'content': 'This is the content of the second blog',
        'author' : 'Test',
        'date' : '10/10/2019'
    }
]


@app.route('/my-first-page')
@app.route('/')
def my_first_page():
    return render_template('home.html')

@app.route('/blogs', methods = ['GET'])
def blogs():
    posts = Post.query.all()
    return render_template('blogs.html', posts=posts, title="Blogs Page")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = User.get_password(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect('/blogs')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            flash('You have successfully logged in!', 'success')
            login_user(user, remember=True)
            return redirect('/blogs')
        else:
            print(form.password.data, user)
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/blogs')


@app.route('/post/<int:post_id>', methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect('/blogs')

@app.route('posts/new/', methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        post = Post(title=request.form.get('title'), content=request.form.get('content'), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect('/blogs')
    else:
        return render_template('create_post.html')

@app.route('posts/<int:post_id>/edit/', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = UpdateForm()
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('You have successfully edited the post!', 'success')
        return redirect('/blogs')
    elif request.method == 'GET':
        return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
