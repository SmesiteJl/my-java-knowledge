# Кэширование в приложении через Spring Cache

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Кэш в памяти приложения: структура данных с временем жизни
* @EnableCaching, @Cacheable, @CachePut
* Имя кэша и ключ; ключи кэша на SpEL: key = #id, key = #product.id
* @CacheEvict и @Caching: инвалидация кэша при изменении данных, allEntries; по каким событиям обновлять кэш
* TTL в Spring Cache: почему в абстракции его нет и как задать через провайдер (Caffeine, RedisCacheManager)
* Почему @Cacheable не срабатывает при self-invocation и при вызове из @PostConstruct
* Cache stampede: что это и как помогает @Cacheable(sync = true)
