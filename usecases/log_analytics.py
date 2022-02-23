import re

from entities import User
from services import datasource
from usecases.add_to_db import AddSourceUseCase, AddOrderUseCase
from usecases.base import BaseUseCase
from usecases.update_db import UpdateSourceUseCase
from usecases.utils import PAID_SOURCES


class AnalyseLogUseCase(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        Метод в таблице с последними платными источниками находит пользователя с тем же client_id, что в data.
        Если такой есть, то его источник обновляется.
        Если нет, то добавляется новая строка.
        После, если есть указатель на наличие заказа, то заказ добавляется в соответсвующую таблицу.
        :param data:
        :return:
        """
        client_id = data['client_id']
        # подменить источник с ссылки на сокращенную версию
        user_row = datasource.session.query(User).filter(User.client_id == client_id).first()
        if user_row:
            self.update_user_source(data)
        else:
            AddSourceUseCase().execute(data)

        if self.is_order(data):
            updated_data = self.update_order_source(data)
            AddOrderUseCase().execute(updated_data)

    @staticmethod
    def is_order(data_from_log: dict) -> bool:
        """
        Если в параметре document.location есть указание на checkout, а в document.referer - на cart,
        считает лог заказом.
        :param data_from_log:
        :return:
        """
        return data_from_log['document.referer'] == "https://shop.com/cart" and (
                data_from_log['document.location'] == "https://shop.com/checkout")

    @staticmethod
    def update_user_source(data_from_log: dict):
        """
        Получает лог, проверяет, какой адрес домена,
        Если по нужному пользователю запись есть, и domain является доменом платного источника,
        то запись в таблице с источниками обновляется.
        Если записи нет, то добавляет запись с текущим значением источника - document.referer
        :param data_from_log:
        :return:
        """
        client_id = data_from_log['client_id']
        user_row = datasource.session.query(User).filter(User.client_id == client_id).first()

        # выделяем домен из document.referer
        string = data_from_log['document.referer']
        pattern = r'^.*\/'
        domain = re.findall(pattern, string)[0]

        # если у юзера уже есть запись в таблице
        if user_row:
            if domain in PAID_SOURCES:
                UpdateSourceUseCase().execute(data_from_log)

        # если у юзера нет записи
        else:
            AddSourceUseCase().execute(data_from_log)

    @staticmethod
    def update_order_source(data_from_log: dict) -> dict:
        """
        Метод обновляет источник поданных данных в соответсвии с источником в таблице User.
        :param data_from_log:
        :return:
        """
        client_id = data_from_log['client_id']
        user_row = datasource.session.query(User).filter(User.client_id == client_id).first()
        data_from_log['document.referer'] = user_row.last_paid_source
        return data_from_log
