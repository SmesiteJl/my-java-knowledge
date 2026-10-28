# Протокол HTTP: запрос и ответ

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Общая логика HTTP: клиент (браузер, мобильное приложение, программа) и веб-сервер, запрос-ответ, отсутствие состояния (stateless)
* Методы HTTP: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, CONNECT, TRACE — назначение каждого
* Безопасные, идемпотентные и неидемпотентные методы
* GET и POST: параметры в query string или в теле; кнопка «Назад», закладки, кэширование, история, ограничение длины и типа данных, видимость, безопасность; кодировки application/x-www-form-urlencoded и multipart/form-data
* Структура запроса и ответа: стартовая строка (метод, путь, версия / версия, код, статус), заголовки, пустая строка, тело
* Основные заголовки: Host, User-Agent, Accept, Accept-Language, Referer, DNT, Connection, Content-Type, Content-Length, Date, Server, X-заголовки (RFC 6648)
* Заголовки кэширования: Last-Modified, ETag, Cache-Control (max-age, must-revalidate, public)
* HTTPS: HTTP поверх TLS/SSL, зачем шифрование, почему SSL заменён на TLS
