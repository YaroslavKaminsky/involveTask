import os
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import requests
from logger import logger
from forms import PaymentForm
import signature
from signature import sign_creator, sign_creator_invoice, sign_creator_bill, order_id_generator


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Yaroslav'
Bootstrap(app)


def pay_method(amount, currency, shop_order_id, description):
    sign = sign_creator(amount, currency, shop_order_id)
    pay_form_data = {
        'amount': amount,
        'currency': currency,
        'shop_id': signature.shop_id,
        'shop_order_id': shop_order_id,
        'sign': sign,
        'description': description
    }
    logger(currency=currency,
           amount=amount,
           description=description,
           order_id=shop_order_id)
    return render_template('pay_form.html', pay_form_data=pay_form_data)


def bill_method(amount, currency, shop_order_id, description):
    sign = sign_creator_bill(amount, currency, shop_order_id)
    bill_data = {
        "description": description,
        "payer_currency": int(currency),
        "shop_amount": amount,
        "shop_currency": int(currency),
        "shop_id": signature.shop_id,
        "shop_order_id": shop_order_id,
        "sign": sign
    }
    response = requests.post('https://core.piastrix.com/bill/create',
                             headers={'Content-Type': 'application/json'},
                             json=bill_data)
    json_response = response.json()
    error_code = json_response['error_code']
    if error_code == 0:
        logger(currency=currency,
               amount=amount,
               description=description,
               order_id=shop_order_id)
        return redirect(json_response['data']['url'])
    else:
        return f'<h1>Error: {json_response["message"]}</h1>'


def invoice_method(amount, currency, shop_order_id, description):
    sign = sign_creator_invoice(amount, currency, shop_order_id)
    raw_invoice_data = {
        'description': description,
        'amount': amount,
        'currency': currency,
        'payway': signature.payway,
        'shop_id': signature.shop_id,
        'shop_order_id': shop_order_id,
        'sign': sign
    }
    response = requests.post('https://core.piastrix.com/invoice/create', json=raw_invoice_data)
    json_response = response.json()
    error_code = json_response['error_code']
    if error_code == 0:
        logger(currency=currency,
               amount=amount,
               description=description,
               order_id=shop_order_id)
        invoice_data = {
            'url': json_response['data']['url'],
            'method': json_response['data']['method'],
            'ac_account_email': json_response['data']['data']['ac_account_email'],
            'ac_sci_name': json_response['data']['data']['ac_sci_name'],
            'ac_amount': json_response['data']['data']['ac_amount'],
            'ac_currency': json_response['data']['data']['ac_currency'],
            'ac_order_id': json_response['data']['data']['ac_order_id'],
            'ac_sign': json_response['data']['data']['ac_sign'],
            'ac_comments': description
        }
        return render_template('invoice_form.html', invoice_data=invoice_data)
    else:
        return f'<h1>Error: {json_response["message"]}</h1>'


@app.route('/', methods=['GET', 'POST'])
def index_page():
    shop_order_id = order_id_generator()
    payment_form = PaymentForm()
    if request.method == 'POST' and payment_form.validate_on_submit():
        amount = payment_form.amount.data
        currency = payment_form.currency.data
        description = payment_form.description.data

        if currency == '978':
            return pay_method(amount, currency, shop_order_id, description)

        elif currency == '840':
            return bill_method(amount, currency, shop_order_id, description)

        elif currency == '643':
            return invoice_method(amount, currency, shop_order_id, description)

    return render_template('index.html', payment_form=payment_form)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
