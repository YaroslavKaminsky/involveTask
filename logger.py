from datetime import datetime


def logger(currency, amount, description, order_id):
    time_ = datetime.now().strftime("%d-%m-%Y %H:%M")
    with open('log.txt', 'a') as log_file:
        log_file.write(f'{time_}. Order ID: {order_id}. Currency: {currency}. Amount: {amount}\n')

if __name__ == '__main__':
    logger('EUR', '20.35', 'sdfsdg', '101')