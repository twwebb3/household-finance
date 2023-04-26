from . import DataRequired, DecimalField, FieldList, FormField, DateField, IntegerField, SelectField, StringField, SubmitField, FlaskForm

class DefaultsDeletionForm(FlaskForm):
    expenditure_type = SelectField('Expenditure Type', choices=[])
    submit3 = SubmitField('Submit')
