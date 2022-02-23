from urllib.parse import urlparse

from entities import User
from services import datasource
from usecases.add_to_db import AddOrderUseCase, AddClientWithSourceUsecase
from usecases.base import BaseUseCase
from usecases.update_db import UpdateSourceForClientUseCase
from usecases.utils import PAID_SOURCES


class AnalyseLogUseCase(BaseUseCase):
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
        # подменить источник с ссылки на сокращенную версию
        user_row: User = datasource.session.query(User).filter(User.client_id == client_id).first()
        if user_row:
            self.update_user_source(data, user_row)
        else:
            AddClientWithSourceUsecase().execute(data)

        if self.is_order(data):
            data['document.referer'] = user_row.last_paid_source
            AddOrderUseCase().execute(data)

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

    @staticmethod
    def update_user_source(data_from_log: dict, user_row: User):
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
        if user_row:
            if domain in PAID_SOURCES:
                UpdateSourceForClientUseCase().execute(data_from_log)

        # если у юзера нет записи
        else:
            AddClientWithSourceUsecase().execute(data_from_log)

