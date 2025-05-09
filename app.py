from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ------------------ HOME ------------------
@app.route('/')
def home():
    return '''
    <h1>Welcome to MMT Cargo Dashboard</h1>
    <ul>
        <li><a href="/sales">Sales</a></li>
        <li><a href="/income">Income</a></li>
        <li><a href="/expenses">Expenses</a></li>
        <li><a href="/withdrawals">Withdrawals</a></li>
        <li><a href="/summary">Summary</a></li>
        <li><a href="/login">Login</a></li>
    </ul>
    '''

# ------------------ SALES ------------------
@app.route('/sales')
def sales():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer, amount, date FROM sales")
    sales_data = cursor.fetchall()
    conn.close()
    return render_template("sales.html", sales=sales_data)

@app.route('/add-sale', methods=['POST'])
def add_sale():
    customer = request.form['customer']
    amount = request.form['amount']
    date = request.form['date']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sales (customer, amount, date) VALUES (?, ?, ?)",
                   (customer, amount, date))
    conn.commit()
    conn.close()
    return redirect('/sales')

# ------------------ INCOME ------------------
@app.route('/income')
def income():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, source, amount, date FROM income")
    income_data = cursor.fetchall()
    conn.close()
    return render_template("income.html", income=income_data)

@app.route('/add-income', methods=['POST'])
def add_income():
    source = request.form['source']
    amount = request.form['amount']
    date = request.form['date']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO income (source, amount, date) VALUES (?, ?, ?)",
                   (source, amount, date))
    conn.commit()
    conn.close()
    return redirect('/income')

# ------------------ EXPENSES ------------------
@app.route('/expenses')
def expenses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, date FROM expenses")
    expense_data = cursor.fetchall()
    conn.close()
    return render_template("expenses.html", expenses=expense_data)

@app.route('/add-expense', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = request.form['amount']
    date = request.form['date']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
                   (category, amount, date))
    conn.commit()
    conn.close()
    return redirect('/expenses')

# ------------------ WITHDRAWALS ------------------
@app.route('/withdrawals')
def withdrawals():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, partner, method, amount, date FROM withdrawals")
    withdrawal_data = cursor.fetchall()
    conn.close()
    return render_template("withdrawals.html", withdrawals=withdrawal_data)

@app.route('/add-withdrawal', methods=['POST'])
def add_withdrawal():
    partner = request.form['partner']
    method = request.form['method']
    amount = request.form['amount']
    date = request.form['date']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO withdrawals (partner, method, amount, date) VALUES (?, ?, ?, ?)",
                   (partner, method, amount, date))
    conn.commit()
    conn.close()
    return redirect('/withdrawals')

# ------------------ SUMMARY ------------------
@app.route('/summary')
def summary():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Totals
    cursor.execute("SELECT SUM(amount) FROM sales")
    total_sales = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM withdrawals")
    total_withdrawals = cursor.fetchone()[0] or 0

    # Partner-wise withdrawal totals
    partners = ["Manager", "Partner 1", "Partner 2", "Partner 3"]
    partner_totals = {}

    for p in partners:
        cursor.execute("SELECT SUM(amount) FROM withdrawals WHERE partner = ?", (p,))
        partner_totals[p] = cursor.fetchone()[0] or 0

    conn.close()

    return render_template("summary.html",
                           total_sales=total_sales,
                           total_income=total_income,
                           total_expenses=total_expenses,
                           total_withdrawals=total_withdrawals,
                           partner_totals=partner_totals)

# ------------------ LOGIN ------------------
@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run()
