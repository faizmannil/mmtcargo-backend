from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/sales')
def sales():
    return render_template("sales.html")

@app.route('/income')
def income():
    return render_template("income.html")

@app.route('/expenses')
def expenses():
    return render_template("expenses.html")

@app.route('/withdrawals')
def withdrawals():
    return render_template("withdrawals.html")

if __name__ == '__main__':
    app.run()
