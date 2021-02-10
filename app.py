import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask.ext.babel import gettext
from wtforms import StringField, SubmitField, DecimalField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# add db for defaults
# need to figure out how to do it row wise
# have two columns, one for expenditure type and one for allotted amount
# db for logging expenditures will be necessary too
# expenditure logs will have date, exp. type, and exp. amt fields at the very least
# class Defaults(db.Model):
#     __tablename__ = 'defaults'
#     id = db.Column(db.Integer, primary_key=True)
#     expenditureType = db.Column(db.String(64), unique=True)
#     amount = db.Column(db.Float, unique=True)
#
#     def __repr__(self):
#         return '<Defaults %r>' % self.expenditureType

class ExpenditureType(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    expType = db.Colum(db.String(64))
    amount = db.relationship(lambda: ExpenditureAmount)

class ExpenditureAmount(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    expTypeId = db.Column(db.Integer(), db.ForeignKey(ExpenditureType.id))
    expenditureAmount = db.Column(db.Float())

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    day = StringField('What is the date?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DefaultsEntryForm(FlaskForm):
    expType = SelectField(gettext("Type"), choices=[(c, c) for c in ['Groceries/Household', 'Alcohol','EatingOut',
                                                                     'Leisure','Gas','Personal Budget']])
    amount = DecimalField("Monthly Allotment:", validators=[DataRequired()])
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(DefaultsEntryForm, self).__init__(csrf_enabled=False, *args, **kwargs)

# determine how to dynamically add forms to total form then load and submit data to db
class DefaultsForm(FlaskForm):
    expDefaults = FieldList(FormField(DefaultsEntryForm), min_entries=1)

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
        #if old_name is not None and old_name != form.name.data:
            #flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        #if old_name is not None and old_name != form.name.data:
            #flash('Looks like you have Analytics!')
        session['name'] = form.name.data
        return redirect(url_for('analytics'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/defaults', methods=['GET', 'POST'])
def defaults():
    form = DefaultsForm()
    if form.validate_on_submit():
        old_name = session.get('gas')
        #if old_name is not None and old_name != form.commute.data:
            #flash('Looks like you have Defaults cuck!')
        session['gas'] = form.commute.data
        return redirect(url_for('defaults'))
    return render_template('index.html', form=form, name=session.get('name'))
