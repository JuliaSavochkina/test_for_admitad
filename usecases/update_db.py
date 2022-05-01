
from repo import UserRepo
from usecases.base import BaseUseCase


class UpdateSourceForClientUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def execute(self, data: dict) -> None:
        """
        В рамках метода осуществляется поиск записи по client_id (такая должна быть одна) в таблице last_source,
        значение последнего платного источника обновляется в соответсвии с поданными данными
        :param data: словарь с данными о последнем источнике для пользователя
        :return:
        """
        client_id = data['client_id']
        self.user_repo.update_last_paid_source(client_id, data['document.referer'])
