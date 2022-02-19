from entities import LastClick
from servises.create_db import session
from usecases.base import BaseUseCase


class UpdateClickLog(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        В рамках метода осуществляется поиск записи по client_id (такая должна быть одна),
        все столбцы записи, кроме client_id обновляются в соответсвии с поданными данными
        :param data: словарь с логом
        :return:
        """
        client_id = data['client_id']
        users_row = session.query(LastClick).filter(LastClick.client_id == client_id)

        users_row.user_agent = data['User-Agent']
        users_row.location = data['document.location'],
        users_row.referer = data['document.referer'],
        users_row.date = data['date']

        session.commit()


class UpdateSourceLog(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        В рамках метода осуществляется поиск записи по client_id (такая должна быть одна) в таблице last_source,
        значение последнего платного источника обновляется в соответсвии с поданными данными
        :param data: словарь с данными о последнем источнике для пользователя
        :return:
        """
        client_id = data['client_id']
        users_row = session.query(LastClick).filter(LastClick.client_id == client_id)

        users_row.last_paid_source = data['last_paid_source']

        session.commit()
