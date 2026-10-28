# Конфигурация Spring Security

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* @EnableWebSecurity и класс конфигурации: WebSecurityConfigurerAdapter в старых версиях и вариант для Security 6 — бин SecurityFilterChain, DaoAuthenticationProvider, authorizeHttpRequests и лямбда-DSL
* AuthenticationManagerBuilder: провайдеры через UserDetailsService, in-memory и JDBC (jdbcAuthentication с usersByUsernameQuery и authoritiesByUsernameQuery); PasswordEncoder и BCryptPasswordEncoder
* HttpSecurity: правила доступа к URL — authorizeRequests, antMatchers, permitAll, hasAuthority; белые и чёрные списки, logout, обработка исключений и accessDeniedPage
* Настройка формы логина: страница, URL обработки, параметры, реакция на успех и ошибку
* CSRF-защита в Spring Security (включена по умолчанию)
* Что изменилось в Spring Security 7: удалены and() и authorizeRequests, только SecurityFilterChain с лямбда-DSL, MFA, Authorization Server внутри Security
