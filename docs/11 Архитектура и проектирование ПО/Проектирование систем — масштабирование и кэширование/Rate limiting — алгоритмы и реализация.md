# Rate limiting: алгоритмы и реализация

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Алгоритмы rate limiting: fixed window, sliding window log/counter, token bucket, leaky bucket — плюсы и минусы каждого
* Распределённый rate limiter: счётчики в Redis (INCR + EXPIRE или Lua-скрипт), где ставить лимитер (gateway или сервис), ответ 429 и Retry-After
