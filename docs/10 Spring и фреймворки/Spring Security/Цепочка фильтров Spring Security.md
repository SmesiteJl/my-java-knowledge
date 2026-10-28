# Цепочка фильтров Spring Security

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Схема аутентификации в коде: UserDetails → токен → AuthenticationManager → SecurityContext, обработка исключения
* DelegatingFilterProxy и FilterChainProxy: мост между сервлетными фильтрами и бинами Spring
* SecurityFilterChain и стандартные фильтры
* Стандартные фильтры: CsrfFilter, LogoutFilter, UsernamePasswordAuthenticationFilter
