from flask import (render_template, url_for, flash, 
                    redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from Blog import db
from Blog.models import Post
from Blog.posts.forms import PostForm
import tmdbsimple as tmdb
tmdb.API_KEY = '272cd66308bce1e18eb99dbe3c664478'

posts = Blueprint('posts', __name__)

@posts.route("/post/new/<int:movie_id>", methods=['GET', 'POST'])
@login_required
def new_post(movie_id):
    
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) #, score=form.score.data
        db.session.add(post)
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend=movie.title)

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been edited!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Edit Post', form=form, legend='Edit Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))