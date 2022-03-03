from sqlalchemy import Column, String

from services import datasource


class User(datasource.Base):
    __tablename__ = 'last_source'

    client_id = Column(String(10), primary_key=True)
    last_paid_source = Column(String)

    def __init__(
            self,
            client_id: str,
            last_paid_source: str
    ) -> None:
        self.client_id = client_id
        self.last_paid_source = last_paid_source

    def __repr__(self):
        return f'user: client_id={self.client_id}, last_paid_source={self.last_paid_source}'
