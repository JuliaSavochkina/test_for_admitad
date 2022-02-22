import logging

from sqlalchemy import update

from entities import LastClick, User
from services import datasource
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
        try:
            to_update = update(LastClick).where(LastClick.client_id == client_id). \
                values(
                {
                    'user_agent': data['User-Agent'],
                    'location': data['document.location'],
                    'referer': data['document.referer'],
                    'date': data['date']
                }
            )
        except Exception as e:
            logging.error(f"Was not able to update this click in DB: because of {e}")
            datasource.session.rollback()  # не ясно как быть с этим
        else:
            datasource.conn.execute(to_update)


class UpdateSourceUseCase(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        В рамках метода осуществляется поиск записи по client_id (такая должна быть одна) в таблице last_source,
        значение последнего платного источника обновляется в соответсвии с поданными данными
        :param data: словарь с данными о последнем источнике для пользователя
        :return:
        """
        client_id = data['client_id']
        try:
            to_update = update(User).where(User.client_id == client_id). \
                values(
                {
                    'last_paid_source': data['document.referer']
                }
            )
        except Exception as e:
            logging.error(f"Was not able to update this source in DB: because of {e}")
            datasource.session.rollback()
        else:
            datasource.conn.execute(to_update)
