from . import DataRequired, DecimalField, FieldList, FormField, DateField, IntegerField, SelectField, StringField, SubmitField, FlaskForm
from .defaults_entry import DefaultsEntryForm


class DefaultsForm(FlaskForm):
    expDefaults = FieldList(FormField(DefaultsEntryForm), min_entries=1)