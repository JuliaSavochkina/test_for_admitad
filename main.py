import logging
from collections import Counter
from datetime import datetime
from typing import List

from flask import Flask, request, jsonify

# импорт для того, чтобы декларативная база знала, какие таблицы создавать
from entities import Order, User
from repo import UserRepo, OrderRepo
from services import Config, datasource
from usecases.generate_stat import get_statistics
from usecases.log_analytics import AnalyseLogUseCase
from usecases.consts import REQUIRED_FIELDS

app = Flask(__name__)
datasource.create_tables()
user_repo = UserRepo(datasource=datasource)
order_repo = OrderRepo(datasource=datasource)
logging.basicConfig(level=Config.LOG_LEVEL)


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
    usecase = AnalyseLogUseCase(user_repo=user_repo, order_repo=order_repo)
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
    Ожидает получить ссылку вида /get_stat?date_from=%Y-%m-%d&date_to=%Y-%m-%d
    :return: json с количеством заказов по выбранным датам
    """
    args = request.args
    date_from = args.get('date_from')
    date_to = args.get('date_to')
    client_id = args.get('client_id')
    if date_from and date_to:
        try:
            prepared_date_from = datetime.strptime(date_from, '%Y-%m-%d')
            prepared_date_to = datetime.strptime(date_to, '%Y-%m-%d')
        except ValueError:
            return jsonify({"status": "Date should be in '%Y-%m-%d'"})
        else:
            amount_of_orders = get_statistics(prepared_date_from, prepared_date_to, client_id)
        return jsonify({f'amount of orders from {date_from} to {date_to}': amount_of_orders})
    else:
        return jsonify({"status": "date_from and date_to should be passed"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
