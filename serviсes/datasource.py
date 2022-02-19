from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from serviсes import POSTGRES_USER, POSTGRES_PASSWORD, HOST, PORT, POSTGRES_DB


class Datasource:
    """
    Класс-обертка, который создает и хранит соединение с базой
    """
    def __init__(self):
        url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{POSTGRES_DB}'
        self.engine = create_engine(url)

        get_session = sessionmaker(bind=self.engine)
        self.session = get_session()
        self.Base = declarative_base()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)

# экземпляр класса, один т.к. достаточно одного соединения с базой
datasource = Datasource()
