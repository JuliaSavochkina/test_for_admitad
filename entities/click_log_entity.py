from sqlalchemy import Column, String, Integer

from servises.create_db import Base


class LastClick(Base):
    __tablename__ = 'last_click'

    id = Column(Integer, primary_key=True)
    client_id = Column(String(10))
    user_agent = Column(String)
    location = Column(String)
    referer = Column(String)
    date = Column(String(30))

    def __init__(
            self,
            client_id: str,
            user_agent: str,
            location: str,
            referer: str,
            date: str
    ) -> None:
        self.client_id = client_id
        self.user_agent = user_agent
        self.location = location
        self.referer = referer
        self.date = date

