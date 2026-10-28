# Actuator, health-пробы и метрики Micrometer

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Свой HealthIndicator и health-группы; какие эндпоинты Actuator нельзя открывать наружу (env, heapdump) и как их защитить
* Graceful shutdown Spring Boot в Kubernetes: server.shutdown=graceful, timeout-per-shutdown-phase, readiness в REFUSING_TRAFFIC; liveness против readiness и почему проверку БД кладут в readiness
* Метрики через Micrometer: Counter, Timer, Gauge, теги и опасность высокой кардинальности; /actuator/prometheus и свои бизнес-метрики
* Трассировка в Spring Boot 3: Micrometer Tracing и OpenTelemetry вместо Sleuth, traceId в логах
