from flask import Flask, redirect, url_for, render_template, request, flash

import os
from os.path import join, dirname
from dotenv import load_dotenv
import braintree

app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app.secret_key = os.environ.get('APP_SECRET_KEY')

braintree.Configuration.configure(
    os.environ.get('BT_ENVIRONMENT'),
    os.environ.get('BT_MERCHANT_ID'),
    os.environ.get('BT_PUBLIC_KEY'),
    os.environ.get('BT_PRIVATE_KEY')
)

print os.environ.get('BT_ENVIRONMENT'), os.environ.get('BT_MERCHANT_ID'), os.environ.get('BT_PUBLIC_KEY'), os.environ.get('BT_PRIVATE_KEY')

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('new_checkout'))

@app.route('/checkouts/new', methods=['GET'])
def new_checkout():
    client_token = braintree.ClientToken.generate()
    return render_template('checkouts/new.html', client_token=client_token)

@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = braintree.Transaction.find(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('checkouts/show.html', transaction=transaction, result=result)

@app.route('/checkouts', methods=['POST'])
def create_checkout():
    import pdb;pdb.set_trace();
    print '/checkouts request form:', request.form
    #result = braintree.Transaction.sale({
    #    'amount': request.form['amount'],
    #    'payment_method_nonce': request.form['payment_method_nonce'],
    #})
    print 'received nonce', request.form['payment_method_nonce']
    result = braintree.Customer.create({
        "first_name": "charity",
        "last_name": "smith",
        'payment_method_nonce': request.form['payment_method_nonce'],
        })
    print 'customer created. customer:', result
    print 'customers payment info:', result.customer.payment_methods
    print 'customer ka payment token:', result.customer.payment_methods[0].token
    print 'deducting 12 dollars from customer acct...'
    result2 = braintree.Transaction.sale({"payment_method_token":
        result.customer.payment_methods[0].token, "amount": "12.00"})
    print 'deduction successful, info of result:', result2
    print ' # TODO(rushiagr): need to handle error scenario in case result2 fails'


    if result.is_success or result.transaction:
        return redirect(url_for('show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567, debug=True)
