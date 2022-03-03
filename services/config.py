import os


class Config:
    """
    В этом классе сосредоточенны все переменные для запуска проекта
    """
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    LOG_LEVEL = int(os.getenv('LOG_LEVEL'))
