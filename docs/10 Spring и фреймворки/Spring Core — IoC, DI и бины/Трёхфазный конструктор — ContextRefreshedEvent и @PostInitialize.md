# Трёхфазный конструктор: ContextRefreshedEvent и @PostInitialize

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Какие события публикует контекст (ContextStarted, ContextStopped, ContextRefreshed) и почему обычно слушают ContextRefreshedEvent
* ApplicationListener с дженериком под конкретный тип события
* Почему @Transactional-логика не работает из @PostConstruct (транзакционный прокси ещё не создан)
* Своя аннотация @PostProxy: вызов методов после построения всех прокси через ApplicationListener
* Почему в листенере нужно читать BeanDefinition через ConfigurableListableBeanFactory, а не делать getBean().getClass() (прокси, lazy-бины)
* Как вызвать метод оригинального класса на прокси: getMethod по имени и типам параметров
* Когда инжектить контекст или фабрику допустимо (инфраструктурный код), а когда это антипаттерн
* Своя аннотация @PostInitialize + ApplicationListener<ContextRefreshedEvent>: вызов метода на прокси, когда транзакционный аспект уже применён
* BPP, дописывающий beanClassName в BeanDefinition для бинов из @Bean-методов (getBeanClassName() == null)
* Почему наполнение БД делают в @EventListener(ContextRefreshedEvent) + @Transactional, а не в @PostConstruct
* @EventListener, объявленный на методе интерфейса; @PreDestroy при закрытии контекста
