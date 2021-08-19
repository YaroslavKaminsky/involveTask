from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import SelectField, TextAreaField, StringField, SubmitField


class PaymentForm(FlaskForm):
    amount = StringField('Сумма оплаты',
                         default='0.00',
                         validators=[
                             validators.required(),
                             validators.none_of(('0.00', '00.00', '00', '0'),
                                                message='Сумма должна быть большей чем 0'),
                             validators.Regexp(r'\d+\.\d{0,2}',
                                               message='Только числа с точностью до двух знаков после запятой')
                         ]
    )
    currency = SelectField('Валюта оплаты',
                           choices=[('840', 'USD'),
                                    ('978', 'EUR'),
                                    ('643', 'RUB')],
                           validators=[validators.required()])
    description = TextAreaField('Описание товара',
                                validators=[validators.required()])
    submit = SubmitField('Оплатить')