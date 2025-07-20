from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    submit = SubmitField('Save')

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    submit = SubmitField('Add Project')

class ExpenseForm(FlaskForm):
    expense_type = StringField('Expense Type', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    item_name = StringField('Item Name', validators=[DataRequired()])
    unit_price = FloatField('Unit Price', validators=[DataRequired()])
    gst_amount = FloatField('GST Amount', validators=[DataRequired()])
    invoice_number = StringField('Invoice Number', validators=[DataRequired()])
    seller_name = StringField('Seller Name', validators=[DataRequired()])
    gstn = StringField('GSTN', validators=[DataRequired()])
    employee_id = SelectField('Employee', coerce=int, validators=[DataRequired()])
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Log Expense')

class RevenueForm(FlaskForm):
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])
    total_estimated_revenue = FloatField('Total Estimated Revenue', validators=[DataRequired()])
    employee_id = SelectField('Employee', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Log Revenue')