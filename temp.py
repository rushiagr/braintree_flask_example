
import os
from os.path import join, dirname
from dotenv import load_dotenv
import braintree

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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

result = braintree.PaymentMethod.create({
    "customer_id": "12345",
    "payment_method_nonce": "fffffffffff",
    })

import pdb;pdb.set_trace();
