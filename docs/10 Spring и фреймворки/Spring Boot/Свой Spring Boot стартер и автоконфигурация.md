# Свой Spring Boot стартер и автоконфигурация

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Как Spring Boot находит автоконфигурации чужого jar (файл .imports, раньше spring.factories)
* Условия @ConditionalOn… и почему бин пользователя побеждает бин стартера
* Стартер ДЗ 1: саморегистрация сервиса по WebServerInitializedEvent и бин DiscoveryClient
* Правила оформления стартера и отладка автоконфигурации
* Почему стартер, а не библиотека с @Component
* Как в ДЗ 1 стартер сам регистрирует сервис? Как работает автоконфигурация?
* Почему бин пользователя побеждает бин стартера?
* Свой стартер: AutoConfiguration.imports, автоконфигурация и свойства
* log-starter: настройки app.logging.* и аннотация @NoLogging
* custom-openapi-starter: не перезаписывает пользовательскую конфигурацию OpenAPI
* spring-boot-starter-jwt-authentication как стартер безопасности для сервисов
* Что приносит стартер: транзитивные зависимости своего «мира» и конфигурации с инфраструктурными бинами
* Почему после подключения нескольких стартеров в контексте сотни бинов
* Как написать свой стартер: конфигурация с бинами плюс регистрация в spring.factories
* Почему стартер не должен требовать @Enable*-аннотаций в приложении (инверсия контроля на уровне модулей)
* Три точки расширения в spring.factories: EnvironmentPostProcessor, ApplicationContextInitializer, EnableAutoConfiguration
* EnvironmentPostProcessor выставляет профиль, если он не задан; инициализатор валит старт без профиля
* @Enable*-аннотация (@EnableIronBankExceptionHandling → @Import) как явная альтернатива автоконфигурации
* Свой Condition (OnProdCondition) с кэшированием ответа в static-поле и аннотация @ConditionOnProd
* Бин advisor только при @ConditionOnProd и @ConditionalOnProperty("raven.destination")
* @ConfigurationProperties(prefix = "raven") + @EnableConfigurationProperties, spring-boot-configuration-processor
* spring.factories: EnableAutoConfiguration, ApplicationContextInitializer, EnvironmentPostProcessor
* Бин MailSender только если у приложения нет своего (@ConditionalOnMissingBean)
* Аспект-обработчик только при заданном свойстве mails.dba (@ConditionalOnProperty)
* Свой Condition с кэшированием результата и мета-аннотация над @Conditional
* EnvironmentPostProcessor ставит профиль по умолчанию, ApplicationContextInitializer проверяет его наличие
* @EnableMyStarter (@Import) как явное подключение конфигурации
* spring.factories → конфигурация с @ComponentScan; мета-аннотация @FrontendRestController и ResponseBodyAdvice для её контроллеров
