from . import DataRequired, DecimalField, FieldList, FormField, DateField, IntegerField, SelectField, StringField, SubmitField, FlaskForm
from datetime import datetime

class ExpenditureEntryForm(FlaskForm):
    type = SelectField('Expenditure Type:', choices=['Mallory Personal Budget', 'TW Personal Budget'])
    store = StringField('Store:', validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    amount = DecimalField('Amount:', validators=[DataRequired()])
    year = IntegerField('Year:', validators=[DataRequired()], default=datetime.now().year)
    month = IntegerField('Month:', validators=[DataRequired()], default=datetime.now().month)
    day = IntegerField('Day:', validators=[DataRequired()], default=datetime.now().day)
    submit = SubmitField('Submit')
