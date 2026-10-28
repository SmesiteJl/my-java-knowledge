# Жизненный цикл бина и scope

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Что такое бин и какой у него жизненный цикл: подготовка (BeanDefinition), создание конструктором, внедрение, BeanPostProcessor (before), инициализация (init-метод), BeanPostProcessor (after), донастройка, уничтожение; где появляется прокси
* Роль BeanFactory: создание объектов по BeanDefinition и хранение синглтонов
* Почему BeanPostProcessor-ы создаются раньше остальных бинов и откладываются «в сторонку»
* Почему в конструкторе нельзя пользоваться тем, что настраивает Spring (NPE или нули)
* Методы инициализации и уничтожения: init-method в XML, @PostConstruct, afterPropertiesSet; @PreDestroy, DisposableBean, destroyMethod
* Объявление бинов через XML-конфигурацию
* Что добавляют в контекст <context:annotation-config/> и <context:component-scan/>; почему @PostConstruct не срабатывает без CommonAnnotationBeanPostProcessor
* Области видимости бина — полный список: singleton, prototype, request, session, application, websocket, общий смысл остальных scopes; чем singleton в Spring отличается от паттерна Singleton
* Scope singleton и prototype: чем отличаются и когда создаются singleton- и prototype-бины
* Почему destroy-метод не вызывается у prototype-бинов
* Задание scope в коде: @Scope с prototype на компоненте и SCOPE_SESSION на @Bean-методе
* Потокобезопасны ли singleton-бины; как быть с изменяемым состоянием (stateless-сервисы, ThreadLocal, request scope)
