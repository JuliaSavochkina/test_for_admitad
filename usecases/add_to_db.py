from entities import LastClick, Order, User
from servises.create_db import session
from usecases.base import BaseUseCase


class AddClick(BaseUseCase):

    def execute(self, data: dict) -> None:
        """
        Метод добавляет запись в таблицу last_click
        :param data: словарь с логм
        :return:
        """
        click = LastClick(
            client_id=data['client_id'],
            user_agent=data['User-Agent'],
            location=data['document.location'],
            referer=data['document.referer'],
            date=data['date']
        )
        session.add(click)
        session.commit()


class AddOrder(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        Метод добавляет запись в таблицу orders
        :param data: словарь с данными по заказу
        :return:
        """
        order = Order(
            client_id=data['client_id'],
            date=data['date'],
            source=data['source']
        )

        session.add(order)
        session.commit()


class AddSource(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        Метод добавляет запись в таблицу last_source
        :param data: словарь с данными по заказу
        :return:
        """
        user = User(
            client_id=data['client_id'],
            last_paid_source=data['last_paid_source'],
        )

        session.add(user)
        session.commit()

