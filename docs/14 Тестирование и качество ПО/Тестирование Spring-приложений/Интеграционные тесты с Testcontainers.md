# Интеграционные тесты с Testcontainers

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Почему API-тест идёт с настоящей БД, а не с моками (источник — документация Testcontainers), и почему H2 вместо реальной БД — плохая идея; @DataJpaTest и @AutoConfigureTestDatabase(replace = NONE)
* Интеграционный стенд: сервис, PostgreSQL и RabbitMQ в контейнерах, заглушка вместо PSP
* Testcontainers со Spring Boot: зависимости (postgresql, junit-jupiter) и копирование миграций в тестовые ресурсы; @Testcontainers и @Container, @DynamicPropertySource против @ServiceConnection (Boot 3.1+), один контейнер на весь набор тестов
* Тесты стартеров, фильтров и провайдеров безопасности
