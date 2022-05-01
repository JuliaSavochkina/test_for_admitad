import logging
from typing import Optional
from urllib.parse import urlparse

from entities import User
from repo import UserRepo, OrderRepo
from usecases.add_to_db import AddClientWithSourceUseCase, AddOrderUseCase
from usecases.base import BaseUseCase
from usecases.consts import PAID_SOURCES


class AnalyseLogUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepo, order_repo: OrderRepo):
        self.user_repo = user_repo
        self.order_repo = order_repo

    def execute(self, data: dict) -> None:
        """
        Метод в таблице с последними платными источниками находит пользователя с тем же client_id, что в data.
        Если такой есть, то его источник обновляется.
        Если нет, то добавляется новая строка.
        После, если есть указатель на наличие заказа, то его источник обновляется в соответсвии с акутальным из таблицы
        User, а заказ добавляется в соответсвующую таблицу.
        :param data: полученный сырой лог
        :return:
        """
        client_id = data['client_id']
        referer = urlparse(data['document.referer'])
        domain = referer.netloc

        user_row: Optional[User] = self.user_repo.get_client_by_id(client_id)
        logging.debug(f'Get {user_row} from User table')
        if user_row:
            self.update_user_source(data, user_row)
        else:
            data['document.referer'] = domain
            AddClientWithSourceUseCase(user_repo=self.user_repo).execute(data)
        # опрашиваем измененную таблицу, страхуем себя от пустой записи
        user_row: Optional[User] = self.user_repo.get_client_by_id(client_id)
        logging.debug(f'Get {user_row} from updated User table')
        if self.is_order(data):
            data['document.referer'] = user_row.last_paid_source
            AddOrderUseCase(order_repo=self.order_repo).execute(data)

    @staticmethod
    def is_order(data_from_log: dict) -> bool:
        """
        Если в параметре document.location есть указание на checkout, а в document.referer - на cart,
        считает лог заказом.
        :param data_from_log: полученный сырой лог
        :return: True если лог является заказом, False, если нет.
        """
        return data_from_log['document.referer'] == "https://shop.com/cart" and (
                data_from_log['document.location'] == "https://shop.com/checkout")

    def update_user_source(self, data_from_log: dict, user_row: Optional[User]):
        """
        Получает лог, проверяет, какой адрес домена,
        Если по нужному пользователю запись есть, и domain является доменом платного источника,
        то запись в таблице с источниками обновляется.
        Если записи нет, то добавляет запись с текущим значением источника - document.referer
        :param data_from_log: полученный сырой лог
        :param user_row: элемент (запись) из таблицы с юзерами
        :return:
        """
        # выделяем домен из document.referer
        referer = urlparse(data_from_log['document.referer'])
        domain = referer.netloc

        # если у юзера уже есть запись в таблице
        if user_row and domain in PAID_SOURCES:
            client_id = data_from_log['client_id']
            self.user_repo.update_last_paid_source(client_id, domain)

        # если у юзера нет записи
        else:
            AddClientWithSourceUseCase(user_repo=self.user_repo).execute(data_from_log)
