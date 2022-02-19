from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


url = f'postgresql://postgres:postgres@localhost:5432/postgres'
engine = create_engine(url)

get_session = sessionmaker(bind=engine)
session = get_session()

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
