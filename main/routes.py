from flask import redirect, render_template, request, Blueprint, current_app, url_for
from Blog.models import Post
from Blog.posts.forms import SearchForm
import tmdbsimple as tmdb
tmdb.API_KEY = '272cd66308bce1e18eb99dbe3c664478'
#tmdb.REQUESTS_SESSION = request.Session()

main = Blueprint('main', __name__)

@main.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/search", methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search = tmdb.Search()
        response = search.movie(query=form.keyword.data) 
        return render_template('search.html', title='Search', form=form,results=search.results)



@main.route("/ranking")
def ranking():
    
    return render_template('ranking.html', title='Top 100')