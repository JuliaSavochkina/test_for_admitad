import logging

from entities import Order, User
from services.datasource import Datasource


class OrderRepo:
    def __init__(self, datasource: Datasource):
        self.db = datasource

    def add_order(self, order: Order):
        try:
            self.db.session.add(order)
            logging.info("Log successfully added")
            self.db.session.commit()
        except Exception as e:
            logging.error(f"Was not able to add this order to DB:{order} because of {e}")
            self.db.session.rollback()


class UserRepo:
    def __init__(self, datasource: Datasource):
        self.db = datasource

    def get_client_by_id(self, _id: str) -> User:
        return self.db.session.query(User).filter(User.client_id == _id).first()

    def update_last_paid_source(self, _id, source: str) -> None:
        try:
            user = self.get_client_by_id(_id)
            user.last_paid_source = source
            self.db.session.commit()
        except Exception as e:
            logging.error(f"Was not able to update this source in DB: because of {e}")
            self.db.session.rollback()

    def add_user(self, user: User):
        try:
            self.db.session.add(user)
            logging.info("Log successfully added")
            self.db.session.commit()
        except Exception as e:
            logging.error(f"Was not able to add this user to DB:{user} because of {e}")
            self.db.session.rollback()
