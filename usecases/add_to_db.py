from entities import Order, User
from repo import OrderRepo, UserRepo
from usecases.base import BaseUseCase


class AddOrderUseCase(BaseUseCase):
    def __init__(self, order_repo: OrderRepo):
        self.order_repo = order_repo

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
        self.order_repo.add_order(order)


class AddClientWithSourceUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

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
        self.user_repo.add_user(user)
