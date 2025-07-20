from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FIX: Added relationships to easily access expenses and revenues submitted by an employee.
    expenses = db.relationship('Expense', backref='employee', lazy=True)
    revenues = db.relationship('Revenue', backref='employee', lazy=True)

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gstn = db.Column(db.String(15), unique=True, nullable=False)

    # FIX: Added relationship to easily access all expenses from a seller.
    expenses = db.relationship('Expense', backref='seller', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    
    # FIX: Changed Float to Numeric for currency to avoid precision errors.
    # Numeric(precision, scale) is the correct type for money.
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    gst_amount = db.Column(db.Numeric(10, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    invoice_number = db.Column(db.String(50), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    updated_flag = db.Column(db.Boolean, default=False)

    # FIX: Added a creation timestamp. This is crucial for time-series forecasting.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationships are correct
    expenses = db.relationship('Expense', backref='project', lazy=True)
    revenues = db.relationship('Revenue', backref='project', lazy=True)

class Revenue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # FIX: Changed Float to Numeric for currency to avoid precision errors.
    total_estimated_revenue = db.Column(db.Numeric(10, 2), nullable=False)
    
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    # FIX: Added a creation timestamp for potential future analysis.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
