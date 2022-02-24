from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from services import Config


class Datasource:
    """
    Класс-обертка, который создает и хранит соединение с базой
    """
    def __init__(self):
        url = f'postgresql://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{Config.HOST}:{Config.PORT}/{Config.POSTGRES_DB}'
        self.engine = create_engine(url)
        self.conn = self.engine.connect()
        get_session = sessionmaker(bind=self.engine)
        self.session = get_session()
        self.Base = declarative_base()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)

# экземпляр класса, один т.к. достаточно одного соединения с базой
datasource = Datasource()
