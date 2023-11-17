from . import DataRequired, DecimalField, FieldList, FormField, DateField, IntegerField, SelectField, StringField, SubmitField, FlaskForm
from datetime import datetime

class BudgetHistoricRemainingForm(FlaskForm):
    expenditure_type = SelectField('Expenditure Type:', choices=['Mallory Personal Budget', 'TW Personal Budget'])
    year = SelectField('Year:',
                       choices=[year for year in range(datetime.now().year-1, datetime.now().year+2)],
                       default=datetime.now().year)
    month = SelectField('Month:',
                        choices=[month for month in range(1, 13)],
                        default=datetime.now().month)
    submit = SubmitField('Submit')