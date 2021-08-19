from hashlib import sha256
import random

shop_id = '5'
secretKey = 'SecretKey01'
payway = 'advcash_rub'


def sign_creator(amount, currency, shop_order_id, shop_id=shop_id, secretKey=secretKey):
    """
    если валюта в выпадающем списке указана “EUR”(978),
    то пользователь направляется на страницу оплаты без выбора направления (по протоколу Pay, стр. 3)
    если валюта указана “USD”(840),
    то осуществляется запрос на выставление счета на оплату по API (метод Bill, стр. 4) в валюте Piastrix.
    """
    signature = f'{amount}:{currency}:{shop_id}:{shop_order_id}{secretKey}'
    return sha256(signature.encode('utf-8')).hexdigest()


def sign_creator_bill(amount, currency, shop_order_id, shop_id=shop_id, secretKey=secretKey):
    """
    если валюта указана “USD”(840),
    то осуществляется запрос на выставление счета на оплату по API (метод Bill, стр. 4) в валюте Piastrix.
    """
    signature = f'{currency}:{amount}:{currency}:{shop_id}:{shop_order_id}{secretKey}'
    return sha256(signature.encode('utf-8')).hexdigest()


def sign_creator_invoice(amount, currency, shop_order_id, payway=payway, shop_id=shop_id, secretKey=secretKey):
    """
    если валюта указана “RUB”,
    то осуществляется запрос на выставление счета на оплату по API (метод Invoice, стр. 6)
    с указанием обязательного параметра payway=advcash_rub.
    """
    signature = f'{amount}:{currency}:{payway}:{shop_id}:{shop_order_id}{secretKey}'
    return sha256(signature.encode('utf-8')).hexdigest()


def order_id_generator():
    return random.randint(100, 10000)



