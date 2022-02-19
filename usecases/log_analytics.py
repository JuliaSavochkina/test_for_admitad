from usecases.base import BaseUseCase


class AnalyseLogUsecase(BaseUseCase):
    def execute(self, data: dict) -> None:
        """
        если в таблице last_click есть запись с юзером того же номера,
        то нужно проверить
        1) источник и обновить таблицу с юзерами
        2) если текущая запись содержить TYP, содержит ли предыдущая card,
        если да, то записать заказ в таблицу с источником из соседней,
        если нет, то просто обновить запись для юзера
        3) если текущая запись не содержит TYP, то обновить запись для юзера
        :param data:
        :return:
        """
        pass


    def is_last_card(self, location: str) -> bool:
        """
        В случае получения TYP, для текущего юзера находит запись в таблице и проверяет,
        является запись лежащая в таблице, корзиной
        :param location:
        :return:
        """
        pass


    def update_last_source(self, referer: str):
        """
        Обновляет таблицу с юзерами новым реферером
        :param referer:
        :return:
        """
        pass


    def update_click(self, click: dict):
        """
        обновляет запись в таблице с предыдущей на текущую
        :param click:
        :return:
        """
        pass
