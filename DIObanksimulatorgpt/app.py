from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Global variables to store account data
account_balance = 0.0
transactions = []

@app.route('/')
def index():
    return render_template('index.html', balance=account_balance)

@app.route('/deposit', methods=['POST'])
def deposit():
    global account_balance
    amount = float(request.form['amount'])
    account_balance += amount
    transactions.append({
        'transaction': 'Deposit',
        'amount': amount,
        'balance': account_balance,
        'datetime': datetime.now()
    })
    return redirect(url_for('index'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    global account_balance
    amount = float(request.form['amount'])
    if amount <= account_balance:
        account_balance -= amount
        transactions.append({
            'transaction': 'Withdrawal',
            'amount': -amount,
            'balance': account_balance,
            'datetime': datetime.now()
        })
        return redirect(url_for('index'))
    else:
        return 'Insufficient funds', 400

@app.route('/statement')
def statement():
    return render_template('statement.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)