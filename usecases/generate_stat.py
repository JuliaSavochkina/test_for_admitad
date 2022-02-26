from datetime import datetime

from entities import Order
from services import datasource


def get_statistics(date_from: datetime, date_to: datetime, client_id: str = ''):
    """
    Выбирает из таблицы с заказами все, принадлежащие нашему источнику и удовлетворяющие указанным датам
    :param date_from:
    :param date_to:
    :param client_id:
    :return:
    """
    if not client_id:
        amount_of_orders = datasource.session.query(Order).filter(Order.date <= date_to). \
            filter(Order.date >= date_from).filter(Order.source == 'referal.ours.com').count()
    else:
        amount_of_orders = datasource.session.query(Order).filter(Order.date <= date_to). \
            filter(Order.date >= date_from).filter(Order.source == 'referal.ours.com'). \
            filter(Order.client_id == client_id).count()
    return amount_of_orders

