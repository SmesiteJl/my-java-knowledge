# HTTP-клиенты в Spring: RestClient, WebClient и HTTP Service Clients

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Почему RestTemplate выводят из употребления и чем его заменить: 7.0 — намерение, 7.1 — @Deprecated, 8.0 — удаление
* RestClient или WebClient: когда блокирующий клиент, когда реактивный, что меняют виртуальные потоки
* @HttpExchange и @ImportHttpServices против OpenFeign: что даёт декларативный клиент и почему Feign объявлен feature-complete
* Таймауты и пул соединений, обработка 4xx и 5xx через onStatus, почему ретраить можно только идемпотентные вызовы
* Как тестировать HTTP-клиент: MockRestServiceServer, WireMock, RestTestClient
