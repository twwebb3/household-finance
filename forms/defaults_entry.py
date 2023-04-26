from . import DataRequired, DecimalField, FieldList, FormField, DateField, IntegerField, SelectField, StringField, SubmitField, FlaskForm


class DefaultsEntryForm(FlaskForm):
    expenditure_type = StringField('Expenditure Type:', validators=[DataRequired()])
    max_amount = DecimalField("Monthly Allotment:", validators=[DataRequired()])
    date_effective = DateField("Date Effective: ", validators=[DataRequired()])
    submit1 = SubmitField('Add')