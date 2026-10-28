# Свой IoC-контейнер с нуля: ObjectFactory, ApplicationContext, конфигураторы

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Как свой контейнер находит реализацию интерфейса: явная карта в конфиге или сканирование Reflections, ошибка при 0 или более чем одной реализации
* Конвейер создания объекта: создать → сконфигурировать (ObjectConfigurator) → вызвать @PostConstruct → обернуть прокси (ProxyConfigurator)
* Кэш синглтонов (@Singleton) в ApplicationContext: чем синглтон отличается от объекта, создаваемого на каждый запрос
* Аналогия с Spring: ObjectConfigurator ≈ BeanPostProcessor, Config ≈ источник BeanDefinition, ApplicationContext ≈ BeanFactory
* Конфиг интерфейс→реализация из config.json плюс сканирование Reflections с ошибками для 0 и более чем одной реализации
* Конвейер ObjectFactory: создать, применить ObjectConfigurator-ы (@InjectByType, @InjectRandomInt), вызвать @PostConstruct, обернуть ProxyConfigurator-ами; кэш @Singleton
* ApplicationContext с кэшем @Singleton и поиском реализации интерфейса, ObjectFactory с конфигураторами @InjectByType и @InjectRandomInt
* Ручные декораторы (TransationalCleaner, BenchmarkProxyCleaner) против динамического прокси для @Benchmark
* Внедрение через единственный конструктор: типы параметров разрешаются из контекста
* Почему контейнер требует ровно один конструктор
* @InjectValue: значение из application.properties по ключу
* ObjectFactory с конфигураторами и ProxyConfigurator для @Benchmark, ApplicationContext с кэшем синглтонов
* ObjectFactory как Singleton: сканирование конфигураторов через Reflections, поиск реализации интерфейса
* ProxyConfigurator для @Benchmark: JDK Proxy при наличии интерфейсов, иначе CGLIB Enhancer
* Включение бенчмарка на лету через MBean (BenchmarkToggle)
