# Resilience-паттерны: timeout, retry с backoff, circuit breaker, bulkhead

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Почему большинство сбоев частичные (медленный внешний сервис, нестабильная сеть, перегруженная БД, растущая очередь) и какие паттерны от них защищают: timeout, retry с ограничением и backoff, circuit breaker, bulkhead
* Timeout: почему один зависший вызов без таймаута блокирует весь пул потоков
* Retry + экспоненциальный backoff с лимитами: как ретраи без таймаутов и лимитов добивают перегруженный сервис и становятся ускорителем инцидента
* Jitter в экспоненциальном backoff и retry storm: почему ретраи на нескольких уровнях умножают нагрузку на упавший сервис
* Circuit breaker: состояния Closed → Open → Half-Open
* Bulkhead: изоляция пулов потоков и соединений между подсистемами
* Rate limit и backpressure: ограничить вход (429), чтобы система оставалась управляемой; повторы клиента с тем же ключом
* Таблица resilience-политик: таймаут, повторы, circuit breaker и fallback для каждого вызова; обоснование чисел — таймаут 1,5 с к PSP, 0 повторов в запросе, bulkhead на 50 одновременных вызовов
* Resilience4j на практике: параметры circuit breaker (sliding window, failureRateThreshold, slowCallRateThreshold, waitDurationInOpenState), порядок декораторов Retry, CircuitBreaker, TimeLimiter и когда он не помогает
* Retry и ограничение конкурентности в Spring 7: @Retryable и @ConcurrencyLimit в ядре; почему Spring Retry убран из dependency management Boot 4; circuit breaker — Resilience4j
