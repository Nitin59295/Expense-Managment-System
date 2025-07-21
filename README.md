ExpensePro: Full-Stack Expense Management System
================================================

A comprehensive full-stack web application built with Python and Flask that allows users to manage project-related expenses and revenues. The system includes secure user authentication, dynamic financial reporting, forecasting, and a professional UI.

🔗 Live Demo
------------
View the live application here: https://expense-pro-app.onrender.com  
(Note: Hosted on a free tier. First-time startup may take 30–60 seconds.)

📌 Key Features
---------------
- ✅ Secure User Authentication: Register/login with secure session handling. User data is isolated and private.
- ✅ Project Management: Create/manage multiple projects with expenses and revenues tied to each.
- ✅ Expense & Revenue Tracking: Add detailed records with item name, quantity, seller, and GST.
- ✅ Data Privacy: Users can only view/manage their own data.
- ✅ Dynamic Reporting: View profit/loss per project, list of sellers, and unique item summaries.
- ✅ Financial Forecasting: ARIMA-based future expense predictions using historical data.
- ✅ Professional UI/UX: Clean, responsive interface with card layout and toast notifications.

🛠️ Technology Stack
--------------------
- Backend: Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login
- Frontend: HTML, CSS, Jinja2
- Database: PostgreSQL
- Data Analysis: Pandas, NumPy, Statsmodels
- Deployment: Render, Gunicorn

🧰 Local Setup and Installation
-------------------------------
1. **Prerequisites**
   - Python 3.10+
   - PostgreSQL installed and running

2. **Clone the Repository**
   ```
   git clone https://github.com/your-username/your-project-name.git
   cd your-project-name
   ```

3. **Create a Virtual Environment**
   - macOS/Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows:
     ```
     python -m venv venv
     .\venv\Scripts\activate
     ```

4. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

5. **Configure the Database**
   - Create a PostgreSQL DB (e.g., `expense_db`)
   - Create a `.env` file in the root folder:
     ```
     DATABASE_URL="postgresql://your_db_user:your_db_password@localhost:5432/expense_db"
     SECRET_KEY="a-very-secret-key-for-flask-sessions"
     ```

6. **Run Migrations**
   ```
   flask db upgrade
   ```

7. **Run the Application**
   ```
   flask run
   ```
   Visit: http://127.0.0.1:5000

🚀 Deployment
--------------
This app is deployed on **Render** with CI/CD enabled. New code pushes to `main` auto-trigger build & database migration.

🖼️ Screenshots
---------------
- **Dashboard**
  ![Dashboard](screenshots/Dashboard.png)
- **Expense Logging Page**
  ![Expense](screenshots/Expense.png)
- **Forecasting**
  ![Forecasting](screenshots/Forecasting.png)
- **Reporting Page**
  ![Report](screenshots/Report.png)

  
📈 Future Improvements
-----------------------
- [ ] Receipt Uploads (image or PDF)
- [ ] Admin Role to view all data
- [ ] Charts & Graphs for financial visualization

---

Developed with ❤️ using Flask and PostgreSQL.
