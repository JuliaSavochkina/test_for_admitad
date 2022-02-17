from typing import Dict

from flask import Flask, request, jsonify

app = Flask(__name__)


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
    content: Dict[str] = request.json
    if check_if_all_params_present(content):
        # создаем экземпляр класса Лог
        log = Log(content)
        # добавляем его в бд
        log.execute()
        return jsonify({"status": "Log added to DB"}), 200
    else:
        return jsonify({"status": "Log is broken"}), 418


@app.route('/get_stat/', methods=['GET'])
def get_stat():
    """
    Эндпоинт для получения статистики.
    Ожидает получить ссылку вида /get_stat/?date_from=%Y-%m-%d&date_to=%Y-%m-%d
    :return: json со статистикой по выбранным датам
    """
    args = request.args
    statistics = get_statistics(args['date_from'], args['date_to'])
    return statistics


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
