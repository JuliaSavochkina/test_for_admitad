import re

from entities import LastClick, User
from services import datasource
from usecases.add_to_db import AddSourceUseCase, AddOrderUseCase, AddClickUseCase
from usecases.base import BaseUseCase
from usecases.update_db import UpdateSourceUseCase, UpdateClickLogUseCase


class AnalyseLogUseCase(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        если в таблице last_click есть запись с юзером того же номера,
        то нужно проверить
        1) источник и обновить таблицу с юзерами
        2) если текущая запись содержить TYP, содержит ли предыдущая card,
        если да, то записать заказ в таблицу с источником из соседней,
        если нет, то просто обновить запись для юзера
        3) если текущая запись не содержит TYP, то обновить запись только для юзера
        :param data:
        :return:
        """
        client_id = data['client_id']
        # подменить источник с ссылки на сокращенную версию
        user_row = datasource.session.query(LastClick).filter(LastClick.client_id == client_id).first()

        if user_row:
            self.update_referer(data)
            if self.is_order(data):
                AddOrderUseCase().execute(data)
            UpdateClickLogUseCase().execute(data)
        else:
            AddClickUseCase().execute(data)
            AddOrderUseCase().execute(data)
            AddSourceUseCase().execute(data)

    @staticmethod
    def is_order(data_from_log: dict) -> bool:
        """
        В случае получения TYP, для текущего юзера находит запись в таблице и проверяет,
        является запись лежащая в таблице, корзиной
        :param data_from_log:
        :return:
        """
        client_id = data_from_log['client_id']
        user_row = datasource.session.query(LastClick).filter(LastClick.client_id == client_id).first()
        loc = user_row.location
        other = data_from_log['document.location']

        return loc == "https://shop.com/cart" and (
                other == "https://shop.com/checkout")

    @staticmethod
    def update_referer(data_from_log: dict):
        """
        Получает лог, проверяет, какой адрес домена,
        Если по нужному пользователю записи нет, то добавляет ее:
        - если "наш" записывает в User.location "ours",
        - если не наш, записывает "theirs1" или "theirs2",
        - если ни один из перечисленных, то "organic".
        Если запись в таблице есть, то обновляет ее только в случае платного истоника.
        :param data_from_log:
        :return:
        """
        client_id = data_from_log['client_id']
        user_row = datasource.session.query(User).filter(User.client_id == client_id).first()

        # выделяем домен из document.referer
        string = data_from_log['document.referer']
        pattern = r'^.*\?'
        domain = re.findall(pattern, string)[0]

        # если у юзера уже есть запись в таблице
        if user_row:
            if domain == "https://referal.ours.com/?":
                data_from_log['document.referer'] = 'ours'
            elif domain == "https://ad.theirs1.com/?":
                data_from_log['document.referer'] = 'theirs1'
            elif domain == "https://ad.theirs2.com/?":
                data_from_log['document.referer'] = 'theirs2'
            UpdateSourceUseCase().execute(data_from_log)

        # если у юзера нет записи
        else:
            if domain == "https://referal.ours.com/?":
                data_from_log['document.referer'] = 'ours'
            elif domain == "https://ad.theirs1.com/?":
                data_from_log['document.referer'] = 'theirs1'
            elif domain == "https://ad.theirs2.com/?":
                data_from_log['document.referer'] = 'theirs2'
            else:
                data_from_log['document.referer'] = 'organic'

            AddSourceUseCase().execute(data_from_log)

    def update_click(self, click: dict):
        """
        обновляет запись в таблице с предыдущей на текущую
        :param click:
        :return:
        """
        pass
