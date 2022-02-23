from collections import Counter
from typing import List

from flask import Flask, request, jsonify

# импорт для того, чтобы декларативная база знала, какие таблицы создавать
from entities import Order, User
from services import datasource
from usecases.generate_stat import get_statistics
from usecases.log_analytics import AnalyseLogUseCase
from usecases.utils import REQUIRED_FIELDS

app = Flask(__name__)
datasource.create_tables()


@app.route('/')
def index():
    response = {
        "status": 200,
        "message": "ok",
    }
    return response


@app.route('/add_log', methods=['POST'])
def add_log():
    """
    Эндпоинт для добавления лога в БД
    :return: сообщение об успешности регистрации лога
    """
    content: List[dict] = request.json
    error_logs = []
    usecase = AnalyseLogUseCase()
    for log in content:
        if Counter(log.keys()) != Counter(REQUIRED_FIELDS):
            error_logs.append(log)
            continue
        usecase.execute(log)

    return jsonify({"status": "Log added to DB",
                    "not processed log(s): ": error_logs}), 200


@app.route('/get_stat', methods=['GET'])
def get_stat():
    """
    Эндпоинт для получения статистики.
    Ожидает получить ссылку вида /get_stat/?date_from=%Y-%m-%d&date_to=%Y-%m-%d
    :return: json со статистикой по выбранным датам
    """
    args = request.args
    # проверка аргументов
    statistics = get_statistics(args['date_from'], args['date_to'])
    return statistics


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
