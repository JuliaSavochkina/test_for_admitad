import logging

from entities import LastClick, Order, User
from services import datasource
from usecases.base import BaseUseCase


class AddOrderUseCase(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        Метод добавляет запись в таблицу orders
        :param data: словарь с данными по заказу
        :return:
        """
        order = Order(
            client_id=data['client_id'],
            date=data['date'],
            source=data['document.referer']
        )

        try:
            datasource.session.add(order)
        except Exception as e:
            # погуглить ошибку
            logging.error(f"Was not able to add this click to DB:{order} because of {e}")
            datasource.session.rollback()
        else:
            datasource.session.commit()


class AddSourceUseCase(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        Метод добавляет запись в таблицу last_source
        :param data: словарь с данными по заказу
        :return:
        """
        user = User(
            client_id=data['client_id'],
            last_paid_source=data['document.referer'],
        )

        try:
            datasource.session.add(user)
        except Exception as e:
            # погуглить ошибку
            logging.error(f"Was not able to add this click to DB:{user} because of {e}")
            datasource.session.rollback()
        else:
            datasource.session.commit()

