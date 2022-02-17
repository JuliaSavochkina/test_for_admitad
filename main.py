from typing import Dict

from flask import Flask, request, jsonify

from servises.create_db import init_connection_to_db, create_db

app = Flask(__name__)
connection = init_connection_to_db()
create_db(connection)


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
    # валидация
    content: Dict[str] = request.json
    add_to_db(content, connection)
    return jsonify({"status": "Log added to DB"}), 200


@app.route('/get_stat/', methods=['GET'])
def get_stat():
    """
    Эндпоинт для получения статистики.
    Ожидает получить ссылку вида /get_stat/?date_from=%Y-%m-%d&date_to=%Y-%m-%d
    :return: json со статистикой по выбранным датам
    """
    args = request.args
    # проверка аргументов
    statistics = get_statistics(args['date_from'], args['date_to'], connection)
    return statistics


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
