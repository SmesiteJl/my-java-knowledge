# @SpringBootApplication и @EnableAutoConfiguration

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Из чего состоит @SpringBootApplication: @SpringBootConfiguration (по сути @Configuration), @EnableAutoConfiguration, @ComponentScan
* Какие пакеты сканирует @ComponentScan главного класса
* Аннотации включения возможностей Spring и Spring Boot: @EnableWebMvc, @EnableAspectJAutoProxy, @EnableCaching, @EnableJpaRepositories, @EnableWebSecurity и @EnableGlobalMethodSecurity
* @EnableAutoConfiguration → @Import(ImportSelector): чем ImportSelector отличается от импорта конфигурации
* Как автоконфигурации сначала загружаются все, а потом отфильтровываются условиями
