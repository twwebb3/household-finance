import os
from datetime import datetime
from flask import Flask, flash, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
# from flask.text.babel import gettext
from wtforms import StringField, SubmitField, DecimalField, FieldList, FormField, DateField
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
    expenditure_type = db.Column(db.String(64), unique=True, index=True)
    max_amount = db.relationship(lambda: ExpenditureAmount)
    date_effective = db.Column(db.DateTime())
    date_ineffective = db.Column(db.DateTime())


class ExpenditureAmount(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    expenditure_type_id = db.Column(db.Integer(), db.ForeignKey(ExpenditureType.id))
    expenditure_date = db.Column(db.DateTime())
    expenditure_amount = db.Column(db.Float())

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    day = StringField('What is the date?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DefaultsEntryForm(FlaskForm):
    expenditure_type = StringField('Expenditure Type:', validators=[DataRequired()])
    amount = DecimalField("Monthly Allotment:", validators=[DataRequired()])
    date_effective = DateField("Date Effective: ", validators=[DataRequired()])
    submit = SubmitField('Add')

# add db references in forms

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
    form = DefaultsEntryForm()
    if form.validate_on_submit():
        expenditure_type = ExpenditureType.query.filter_by(expenditure_type=form.expenditure_type.data).first()
        if expenditure_type is None:
            expenditure_type = ExpenditureType(expenditure_type=form.expenditure_type.data)
            db.session.add(expenditure_type)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            flash('That default already exists cuck!')
        session['expenditure_type'] = form.expenditure_type.data
        #if old_name is not None and old_name != form.commute.data:
            #flash('Looks like you have Defaults cuck!')
        return redirect(url_for('defaults'))
    return render_template('index.html', form=form, expenditure_type=session.get('expenditure_type'))
