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

Известно, что есть три кешбэк-сервиса, с которых пользователи могут попадать в магазин: наш сервис referal.ours.com и два конкурента ad.theirs1.com и ad.theirs2.com.

Считается, что пользователь совершил заказ, если он попал на страницу магазина https://shop.com/checkout со страницы https://shop.com/cart.

Считается, что заказ принадлежит тому кэшбек-сервису, переход с которого был последним в цепочке переходов пользователя.
