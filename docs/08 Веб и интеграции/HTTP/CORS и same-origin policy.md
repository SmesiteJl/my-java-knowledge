# CORS и same-origin policy

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Same-origin policy и зачем нужен CORS
* Заголовок Origin и ответные заголовки Access-Control-Allow-Origin, -Methods, -Headers, -Credentials, Access-Control-Max-Age
* Preflight-запрос OPTIONS: какие запросы считаются простыми, когда браузер отправляет preflight и как кэшируется ответ
* fetch с credentials: 'include' и настройка CORS на сервере
* Почему CORS не защищает сервер от запросов (это политика браузера) и чем опасны Access-Control-Allow-Origin: * или отражение Origin вместе с credentials
