from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    day = StringField('What is the date?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DefaultsForm(FlaskForm):
    commuteExpenses = StringField("Gas/Tolls:", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have Analytics!')
        session['name'] = form.name.data
        return redirect(url_for('analytics'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/defaults', methods=['GET', 'POST'])
def defaults():
    form = DefaultsForm()
    if form.validate_on_submit():
        old_name = session.get('gas')
        if old_name is not None and old_name != form.commuteExpenses.data:
            flash('Looks like you have Defaults cuck!')
        session['gas'] = form.commuteExpenses.data
        return redirect(url_for('defaults'))
    return render_template('index.html', form=form, name=session.get('name'))
