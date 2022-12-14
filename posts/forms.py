from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    #score = IntegerField('Score', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    submit = SubmitField('Submit')