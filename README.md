Приложение представляет собой сервис матчинга, который по логам ищет заказы каких пользователей принадлежат нашему кэшбеку.

## Бизнес логика  
Пользователи приходят в онлайн-магазин shop.com, где совершают заказы.

У нас есть доступ к логам переходов пользователей вида
```
[
  {
	"client_id": "user15",
    "User-Agent": "Firefox 80",
	"document.location": "https://shop.com/products/?id=2",
	"document.referer": "https://yandex.ru/search/?q=купить+котика",
	"date": "2021-04-03T07:59:13.286000Z"
  },
  {
      "client_id": "user15",
      "User-Agent": "Firefox 80",
      "document.location": "https://shop.com/products/?id=2",
      "document.referer": "https://referal.ours.com/?ref=123hexcode",
      "date": "2021-04-04T08:30:14.104000Z"
  },
  {
      "client_id": "user15",
      "User-Agent": "Firefox 80",
      "document.location": "https://shop.com/products/?id=2",
      "document.referer": "https://referal.ours.com/?ref=123hexcode",
      "date": "2021-04-04T08:45:14.384000Z"
  },
  {
      "client_id": "user15",
      "User-Agent": "Firefox 80",
      "document.location": "https://shop.com/checkout",
      "document.referer": "https://shop.com/products/?id=2",
      "date": "2021-04-04T08:59:16.222000Z"
  },
  {
	"client_id": "user7",
	"User-Agent": "Chrome 92",
	"document.location": "https://shop.com/",
	"document.referer": "https://referal.ours.com/?ref=0xc0ffee",
	"date": "2021-05-23T18:59:13.286000Z"
  },
  ...
]
```

Известно, что есть три кешбэк-сервиса, с которых пользователи могут попадать в магазин: наш сервис `referal.ours.com` и два конкурента `ad.theirs1.com` и `ad.theirs2.com`.

Считается, что пользователь совершил заказ, если он попал на страницу магазина `https://shop.com/checkout` со страницы `https://shop.com/cart`.

Считается, что заказ принадлежит тому кэшбек-сервису, переход с которого был последним в цепочке переходов пользователя.


## Логика проекта
Проект стартует в файле `main.py`, где описана работа эндпоинтов и создается Flask-приложение.

### Эндпоинты проекта
/**add_log** - отвечает за работу с сырыми логами, переданными со стороны клиента. Анализирует их и распределяет данные по таблицам.
```
curl --location --request POST 'http://0.0.0.0:5000/add_log' \
--header 'Content-Type: application/json' \
--data-raw '[
  {
	"client_id": "user15",
    "User-Agent": "Firefox 80",
	"document.location": "https://shop.com/products/?id=2",
	"document.referer": "https://yandex.ru/search/?q=купить+котика",
	"date": "2021-04-03T07:59:13.286000Z"
  },
  ...
]'
```
Ожидает получить данные `POST` методом в `json` формате. Далее данные передаются в класс `AnalyseLogUseCase` где происходит нельколько дейсвтий.
* В зависимости от наличия записи о текущем пользователе, в таблице с последним платным источником она либо появляется, либо обновляется по принципу LCW.
* В случае если лог отправлен со страницы `checkout` и в качестве реферера значится страница корзины, такой лог считается заказом и заказа записывается в таблицу с заказами, параллельно источник подменяется на последний платный из соседней таблицы.  
В таблице хранятся все заказы.

/**get_stat** - отвечает за получение статистики. Ожидает запрос в формате `/get_stat?date_from=%Y-%m-%d&date_to=%Y-%m-%d`, возвращает количество заказов за указанный период. Допоплнительно можно передать номер клиента в параметре `client_id` и получить количество заказов только по нему.
```
curl --location --request GET 'http://0.0.0.0:5000/get_stat?date_from=2021-04-30&date_to=2021-06-30&client_id=user7'
```

Ожидает получить данные методом `GET`. Далее идет выбор из таблицы с заказами тех, что являются "нашими" за указанные даты. Дополнительно можно указать фильтр по клиенту.

## Технологии в проекте
В проекте использована база данных `PostgreSQL` с двумя таблицами. Таблицы можно посмотреть через `adminer` - http://localhost:8080/.
![](https://i.imgur.com/kAehrMI.png)

## Приступая к работе
Склонируйте проект на свой компьютер.

### Запуск проекта
```shell script
docker-compose up --build
```
 или через `make run`.

### Тестирование
Тесты локально запускаются командой
```shell script
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

или через `make test`. Команда запускает тест в контейнере.


### Remote debug

1. Настройте интерпретатор:
* File -> Settings -> Python Interpreter
* Добавьте новый типа Docker Compose так, как на скрине ниже:
![](https://i.imgur.com/MWslTTi.png)
* Настройте маппинг:
![](https://i.imgur.com/2JH9uwx.png)
  Примените и сохраните настройки.

2. Настройте конфигурацию:
* Добавьте новую  
![](https://i.imgur.com/fUapLDh.png)  
типа Python  
![](https://i.imgur.com/0n8mkfM.png) 

* Настройте новую конфигурацию, как на скрине  
![](https://i.imgur.com/Ag70Nmm.png)

* примените и сохраните.  