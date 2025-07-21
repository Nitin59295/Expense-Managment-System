from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User

# New form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

# New form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

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
    # FIX: Removed employee_id field
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Log Expense')

class RevenueForm(FlaskForm):
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])
    total_estimated_revenue = FloatField('Total Estimated Revenue', validators=[DataRequired()])
    # FIX: Removed employee_id field
    submit = SubmitField('Log Revenue')
