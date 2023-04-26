from . import DataRequired, DecimalField, FieldList, FormField, DateField, IntegerField, SelectField, StringField, SubmitField, FlaskForm

class DefaultsViewingForm(FlaskForm):
    expenditure_type = SelectField('Expenditure Type', choices=[])
    submit2 = SubmitField('Submit')
