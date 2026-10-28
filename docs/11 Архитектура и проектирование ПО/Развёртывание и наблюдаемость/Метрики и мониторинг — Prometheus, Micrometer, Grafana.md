# Метрики и мониторинг: Prometheus, Micrometer, Grafana

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Зачем мониторинг и как работает Prometheus: pull-модель, scrape эндпоинта /actuator/prometheus, временные ряды и лейблы, дашборды в Grafana
* Типы метрик Prometheus: counter, gauge, histogram, summary — какой взять для заказов в секунду и для latency (rate, histogram_quantile)
* Кастомные бизнес-метрики через Micrometer (Counter, Timer, Gauge, MeterRegistry) и почему опасна высокая кардинальность лейблов
