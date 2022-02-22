import logging

from sqlalchemy import update

from entities import User
from services import datasource
from usecases.base import BaseUseCase


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
