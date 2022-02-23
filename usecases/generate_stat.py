from datetime import datetime

from entities import Order
from services import datasource


def get_statistics(date_from: str, date_to: str):
    """
    Выбирает из таблицы с заказами все, принадлежащие нашему источнику и
    удовлетворяющие указанным датам
    :param date_from:
    :param date_to:
    :return:
    """
    prepared_date_from = datetime.strptime(date_from, '%Y-%m-%d')
    prepared_date_to = datetime.strptime(date_to, '%Y-%m-%d')
    amount_of_orders = datasource.session.query(Order).filter(Order.date <= prepared_date_to). \
        filter(Order.date >= prepared_date_from).filter(Order.source == 'referal.ours.com').count()
    return amount_of_orders

