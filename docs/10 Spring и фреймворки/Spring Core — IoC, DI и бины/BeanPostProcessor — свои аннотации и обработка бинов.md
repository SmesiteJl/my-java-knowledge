# BeanPostProcessor: свои аннотации и обработка бинов

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Назначение BeanPostProcessor и связь с паттерном Chain of Responsibility
* Методы postProcessBeforeInitialization и postProcessAfterInitialization: когда вызываются и что могут вернуть; зачем две фазы и почему подмена класса делается в postProcessAfterInitialization
* Своя аннотация и её обработчик: @InjectRandomInt и InjectRandomIntAnnotationBeanPostProcessor (обход полей через рефлексию, ReflectionUtils.setField)
* Как зарегистрировать свой BeanPostProcessor в контексте; почему инфраструктурному бину не нужен id
* Какие стандартные BPP обрабатывают @Autowired и @PostConstruct (AutowiredAnnotationBeanPostProcessor, CommonAnnotationBeanPostProcessor)
* @InjectByType: инъекция поля объектом из контекста через рефлексию
* @InjectProperty: чтение application.properties и инъекция значения по ключу или имени поля
* Как BPP по списку классов из аннотации достаёт бины из контекста и кладёт список в поле
* Свой @InjectListOfBeans: BPP собирает бины по классам и порядку из аннотации
* BPP для своей аннотации @InjectChuckNorrisQuote: инъекция значения в поле до init-метода
* Профилирование методов через прокси с замером времени (System.nanoTime) и включением на лету
* Почему BPP, читающий аннотации класса, должен работать с оригинальным классом, а не с прокси; как запомнить оригинальный класс по имени бина в before-фазе и создать прокси в after-фазе
* Мета-аннотации: @EbayService = @Service + @Transactional, @EbayAutowired = @Autowired
* @InjectRandomName / @InjectRandomInt: BPP заполняет поле в postProcessBeforeInitialization
