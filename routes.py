"""
Defines all application routes and view functions.
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import db, User, Seller, Project, Expense, Revenue
from forms import LoginForm, RegistrationForm, ProjectForm, ExpenseForm, RevenueForm
from sqlalchemy import func
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import datetime, timedelta

routes = Blueprint('routes', __name__)

# --- Authentication Routes ---
# (No changes here)
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('routes.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', title='Sign In', form=form)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, designation=form.designation.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

# --- Core Application Routes (Protected) ---

@routes.route('/')
@routes.route('/index')
@login_required
def index():
    return render_template('index.html')

@routes.route('/expenses', methods=['GET', 'POST'])
@login_required
def log_expenses():
    form = ExpenseForm()
    # FIX: The project dropdown should only show projects created by the current user.
    form.project_id.choices = [(p.id, p.name) for p in Project.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        # ... (rest of the logic is correct)
        try:
            seller = Seller.query.filter_by(gstn=form.gstn.data.strip()).first()
            if not seller:
                seller = Seller(name=form.seller_name.data.strip(), gstn=form.gstn.data.strip())
                db.session.add(seller)
            project = Project.query.get(form.project_id.data)
            total_amount = (Decimal(form.unit_price.data) * Decimal(form.quantity.data)) + Decimal(form.gst_amount.data)
            expense = Expense(
                expense_type=form.expense_type.data,
                item_name=form.item_name.data.strip(),
                quantity=form.quantity.data,
                unit_price=form.unit_price.data,
                gst_amount=form.gst_amount.data,
                total_amount=total_amount,
                invoice_number=form.invoice_number.data.strip(),
                seller=seller,
                project=project,
                user=current_user
            )
            db.session.add(expense)
            db.session.commit()
            flash('Expense logged successfully!', 'success')
            return redirect(url_for('routes.log_expenses'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", 'danger')
      
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.created_at.desc()).all()
    return render_template('expenses.html', form=form, expenses=expenses)
    
@routes.route('/revenue', methods=['GET', 'POST'])
@login_required
def log_revenue():
    form = RevenueForm()
    # FIX: The project dropdown should also be filtered here.
    form.project_id.choices = [(p.id, p.name) for p in Project.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        project = Project.query.get(form.project_id.data)
        revenue = Revenue(
            total_estimated_revenue=form.total_estimated_revenue.data,
            project=project,
            user=current_user
        )
        db.session.add(revenue)
        db.session.commit()
        flash('Revenue logged successfully!', 'success')
        return redirect(url_for('routes.log_revenue'))
    revenues = Revenue.query.filter_by(user_id=current_user.id).order_by(Revenue.created_at.desc()).all()
    return render_template('revenue.html', form=form, revenues=revenues)

@routes.route('/projects', methods=['GET', 'POST'])
@login_required
def manage_projects():
    form = ProjectForm()
    if form.validate_on_submit():
        # FIX: When creating a new project, assign it to the current user.
        project = Project(name=form.name.data, user=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('routes.manage_projects'))

    # FIX: Only show the projects created by the logged-in user.
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html', form=form, projects=projects)

# ... (The rest of the routes are already correctly filtered by user_id)
@routes.route('/projects/<int:id>')
@login_required
def view_project(id):
    # This query ensures a user can only view their own projects
    project = Project.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    expenses = Expense.query.filter_by(project_id=id, user_id=current_user.id).all()
    revenues = Revenue.query.filter_by(project_id=id, user_id=current_user.id).all()
    total_expenses = sum(e.total_amount for e in expenses)
    total_revenues = sum(r.total_estimated_revenue for r in revenues)
    return render_template('view_project.html', project=project, expenses=expenses,
                           revenues=revenues, total_expenses=total_expenses,
                           total_revenues=total_revenues)

@routes.route('/report')
@login_required
def report():
    project_reports_query = db.session.query(
        Project.name,
        func.sum(Expense.total_amount).label('total_expenses'),
        func.sum(Revenue.total_estimated_revenue).label('total_revenues')
    ).select_from(Project)\
    .filter(Project.user_id == current_user.id) \
    .outerjoin(Expense, (Project.id == Expense.project_id))\
    .outerjoin(Revenue, (Project.id == Revenue.project_id))\
    .group_by(Project.name)\
    .all()
    project_reports = [
        {'name': name, 'total_expenses': expenses or 0, 'total_revenues': revenues or 0}
        for name, expenses, revenues in project_reports_query
    ]
    sellers = Seller.query.join(Expense).filter(Expense.user_id == current_user.id).distinct().all()
    item_names_tuples = db.session.query(Expense.item_name).filter(Expense.user_id == current_user.id).distinct().all()
    items = [item[0] for item in item_names_tuples if item[0]]
    return render_template('report.html', project_reports=project_reports, sellers=sellers, items=items)

@routes.route('/forecast')
@login_required
def forecast():
    expenses_over_time = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.created_at).all()
    if len(expenses_over_time) < 10:
        flash("Not enough expense data for a reliable forecast.", "warning")
        return redirect(url_for('routes.index'))
    data = {exp.created_at: float(exp.total_amount) for exp in expenses_over_time}
    series = pd.Series(data)
    daily_series = series.resample('D').sum()
    if len(daily_series[daily_series > 0]) < 5:
        flash("Generating a demo forecast with sample historical data.", "info")
        today = datetime.now()
        fake_data = {
            today - timedelta(days=i): np.random.uniform(10000, 50000) for i in range(1, 11)
        }
        todays_total = daily_series.sum()
        if todays_total > 0:
            fake_data[today] = todays_total
        daily_series = pd.Series(fake_data)
    log_transformed_series = np.log(daily_series[daily_series > 0])
    try:
        model = ARIMA(log_transformed_series, order=(1, 1, 1))
        model_fit = model.fit()
        forecast_result = model_fit.forecast(steps=7)
        inverse_transformed_forecast = np.exp(forecast_result)
        formatted_forecast = {
            date.strftime('%Y-%m-%d'): round(value, 2)
            for date, value in inverse_transformed_forecast.items()
        }
        return render_template('forecast.html', forecast=formatted_forecast)
    except Exception as e:
        flash(f"Could not generate forecast: {e}", "danger")
        return redirect(url_for('routes.index'))
