import os
import pandas as pd
from datetime import datetime
from flask import Flask, flash, render_template, session, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
# from flask.text.babel import gettext
from wtforms import StringField, SubmitField, DecimalField, FieldList, FormField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from data import db_query

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
    max_amount = db.Column(db.Float())
    date_effective = db.Column(db.DateTime())
    date_ineffective = db.Column(db.DateTime())

    def __repr__(self):
        return '<ExpenditureType %r>' % self.expenditure_type


class ExpenditureAmount(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    type_id = db.Column(db.Integer(), db.ForeignKey(ExpenditureType.id))
    type = db.Column(db.String(64))
    store = db.Column(db.String(64))
    description = db.Column(db.String(200))
    amount = db.Column(db.Float())
    year = db.Column(db.Integer())
    month = db.Column(db.Integer())
    day = db.Column(db.Integer())

    def __repr__(self):
        return '<ExpenditureAmount %r>' % self.amount


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    day = StringField('What is the date?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BudgetRemainingForm(FlaskForm):
    expenditure_type = SelectField('Expenditure Type:', choices=['Mallory Personal Budget', 'TW Personal Budget'])
    submit = SubmitField('Submit')


class BudgetHistoricRemainingForm(FlaskForm):
    expenditure_type = SelectField('Expenditure Type:', choices=['Mallory Personal Budget', 'TW Personal Budget'])
    year = SelectField('Year:',
                       choices=[year for year in range(datetime.now().year-1, datetime.now().year+2)],
                       default=datetime.now().year)
    month = SelectField('Month:',
                        choices=[month for month in range(1, 13)],
                        default=datetime.now().month)
    submit = SubmitField('Submit')


class DefaultsEntryForm(FlaskForm):
    expenditure_type = StringField('Expenditure Type:', validators=[DataRequired()])
    max_amount = DecimalField("Monthly Allotment:", validators=[DataRequired()])
    date_effective = DateField("Date Effective: ", validators=[DataRequired()])
    submit1 = SubmitField('Add')


class DefaultsViewingForm(FlaskForm):
    expenditure_type = SelectField('Expenditure Type', choices=[])
    submit2 = SubmitField('Submit')


class DefaultsDeletionForm(FlaskForm):
    expenditure_type = SelectField('Expenditure Type', choices=[])
    submit3 = SubmitField('Submit')


class ExpenditureEntryForm(FlaskForm):
    type = SelectField('Expenditure Type:', choices=['Mallory Personal Budget', 'TW Personal Budget'])
    store = StringField('Store:', validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    amount = DecimalField('Amount:', validators=[DataRequired()])
    year = IntegerField('Year:', validators=[DataRequired()], default=datetime.now().year)
    month = IntegerField('Month:', validators=[DataRequired()], default=datetime.now().month)
    day = IntegerField('Day:', validators=[DataRequired()], default=datetime.now().day)
    submit = SubmitField('Submit')

# add db references in forms


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
    form = BudgetRemainingForm()

    exp1 = ExpenditureType.query.with_entities(ExpenditureType.expenditure_type)
    exp_type = []
    for j in exp1:
        temp = j._asdict()
        exp_type.append(temp['expenditure_type'])

    form.expenditure_type.choices = exp_type

    amount = ''
    exp_hist_df = pd.DataFrame({})
    if form.validate_on_submit():
        exp_hist_df = db_query.extract_expenditure_history(ExpenditureAmount=ExpenditureAmount,
                                                           type=form.expenditure_type.data,
                                                           year=datetime.now().year,
                                                           month=datetime.now().month)

        amount = db_query.budget_remaining(ExpenditureType=ExpenditureType,
                                           ExpenditureAmount=ExpenditureAmount,
                                           type=form.expenditure_type.data)

    sample_table = pd.DataFrame({'cool': [1, 2, 3], 'not cool': ['a', 'b', 'abc']})

    return render_template('index.html',
                           form=form,
                           amount=amount,
                           tables=[exp_hist_df.to_html(classes='data')])


@app.route('/expenditure_history', methods=['GET', 'POST'])
def history():
    form = BudgetHistoricRemainingForm()

    exp1 = ExpenditureType.query.with_entities(ExpenditureType.expenditure_type)
    exp_type = []
    for j in exp1:
        temp = j._asdict()
        exp_type.append(temp['expenditure_type'])

    form.expenditure_type.choices = exp_type

    amount=''
    exp_hist_df = pd.DataFrame({})
    if form.validate_on_submit():
        exp_hist_df = db_query.extract_expenditure_history(ExpenditureAmount = ExpenditureAmount,
                                                           type = form.expenditure_type.data,
                                                           year = form.year.data,
                                                           month = form.month.data)

        amount = db_query.budget_remaining(ExpenditureType=ExpenditureType,
                                           ExpenditureAmount=ExpenditureAmount,
                                           type=form.expenditure_type.data)

    sample_table = pd.DataFrame({'cool': [1, 2, 3], 'not cool': ['a', 'b', 'abc']})

    return render_template('index.html',
                           page_header="Expenditure History",
                           form=form,
                           amount=amount,
                           table_name="Historic Expenditures",
                           tables=[exp_hist_df.to_html(classes='data')],
                           titles=sample_table.columns.values)


@app.route('/expenditure_entry', methods=['GET', 'POST'])
def entry():
    form = ExpenditureEntryForm()

    exp1 = ExpenditureType.query.with_entities(ExpenditureType.expenditure_type)
    exp_type = []
    for j in exp1:
        temp = j._asdict()
        exp_type.append(temp['expenditure_type'])

    form.type.choices = exp_type

    if form.validate_on_submit():
        expenditure_amount = ExpenditureAmount(type=form.type.data,
                                               store=form.store.data,
                                               description=form.description.data,
                                               amount=form.amount.data,
                                               year=form.year.data,
                                               month=form.month.data,
                                               day=form.day.data)
        db.session.add(expenditure_amount)
        db.session.commit()
    return render_template('index.html',
                           page_header="Expenditure Entry",
                           form=form,
                           name=session.get('name'))


@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        session['name'] = form.name.data
        return redirect(url_for('analytics'))
    return render_template('index.html', form=form, name=session.get('name'), amount=0)


@app.route('/defaults', methods=['GET', 'POST'])
def defaults():
    # if 'expenditure_type' not in session:
    session['expenditure_type'] = []
    form = DefaultsEntryForm()
    form2 = DefaultsViewingForm()
    form3 = DefaultsDeletionForm()

    amount = ''

    exp1 = ExpenditureType.query.with_entities(ExpenditureType.expenditure_type)
    exp_type = []
    for j in exp1:
        temp = j._asdict()
        exp_type.append(temp['expenditure_type'])

    form2.expenditure_type.choices = exp_type
    form3.expenditure_type.choices = exp_type

    if form.submit1.data and form.validate():
        expenditure_type = ExpenditureType.query.filter_by(expenditure_type=form.expenditure_type.data).first()
        print(ExpenditureType.query.filter_by(expenditure_type=form.expenditure_type.data).first())
        # expenditure_type_list = session['expenditure_type']
        # for exp in expenditure_type:
        #     if exp not in expenditure_type_list:
        #         expenditure_type_list.append(expenditure_type)
        # session['expenditure_type'] = expenditure_type_list
        if expenditure_type is None:
            print(form.expenditure_type.data)
            expenditure_type = ExpenditureType(expenditure_type=form.expenditure_type.data,
                                               max_amount=form.max_amount.data,
                                               date_effective=form.date_effective.data)
            # print(form.expenditure_type.data)
            db.session.add(expenditure_type)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            flash('That default already exists cuck!')
        # session['expenditure_type'] = jsonify(expenditure_type_list)
        # if old_name is not None and old_name != form.commute.data:
            # flash('Looks like you have Defaults cuck!')
        return redirect(url_for('defaults'))


    if form2.submit2.data and form2.validate():
        exp1 = ExpenditureType.query.with_entities(ExpenditureType.expenditure_type,
                                                   ExpenditureType.max_amount)
        max_amount = 0
        for j in exp1:
            temp = j._asdict()
            if temp['expenditure_type']==form2.expenditure_type.data:
                max_amount = temp['max_amount']

        amount = max_amount

    if form3.submit3.data and form3.validate_on_submit():
        exp_type = form3.expenditure_type.data

        ExpenditureType.query.filter_by(expenditure_type=exp_type).delete()

        db.session.commit()


    return render_template('defaults.html',
                           form=form,
                           form2=form2,
                           form3=form3,
                           expenditure_amount=amount)
