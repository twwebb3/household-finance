from . import DataRequired, DecimalField, FieldList, FormField, DateField, IntegerField, SelectField, StringField, SubmitField, FlaskForm

class BudgetRemainingForm(FlaskForm):
    expenditure_type = SelectField('Expenditure Type:', choices=['Mallory Personal Budget', 'TW Personal Budget'])
    submit = SubmitField('Submit')
