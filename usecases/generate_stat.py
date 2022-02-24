from datetime import datetime

from entities import Order
from services import datasource


class GetStatistics:
    @staticmethod
    def get_statistics(date_from: datetime, date_to: datetime):
        """
        Выбирает из таблицы с заказами все, принадлежащие нашему источнику и
        удовлетворяющие указанным датам
        :param date_from:
        :param date_to:
        :return:
        """

        amount_of_orders = datasource.session.query(Order).filter(Order.date <= date_to). \
            filter(Order.date >= date_from).filter(Order.source == 'referal.ours.com').count()
        return amount_of_orders

