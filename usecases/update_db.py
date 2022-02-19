import logging

from entities import LastClick
from serviсes import datasource
from usecases.base import BaseUseCase


class UpdateClickLogUseCase(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        В рамках метода осуществляется поиск записи по client_id (такая должна быть одна),
        все столбцы записи, кроме client_id обновляются в соответсвии с поданными данными
        :param data: словарь с логом
        :return:
        """
        client_id = data['client_id']
        users_row = datasource.session.query(LastClick).filter(LastClick.client_id == client_id)
        try:
            users_row.user_agent = data['User-Agent']
            users_row.location = data['document.location'],
            users_row.referer = data['document.referer'],
            users_row.date = data['date']
        except Exception as e:
            logging.error(f"Was not able to update this click in DB:{users_row} because of {e}")
            datasource.session.rollback()
        else:
            datasource.session.commit()


class UpdateSourceLogUseCase(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        В рамках метода осуществляется поиск записи по client_id (такая должна быть одна) в таблице last_source,
        значение последнего платного источника обновляется в соответсвии с поданными данными
        :param data: словарь с данными о последнем источнике для пользователя
        :return:
        """
        client_id = data['client_id']
        users_row = datasource.session.query(LastClick).filter(LastClick.client_id == client_id)
        try:
            users_row.last_paid_source = data['last_paid_source']
        except Exception as e:
            logging.error(f"Was not able to update this source in DB:{users_row} because of {e}")
            datasource.session.rollback()
        else:
            datasource.session.commit()
