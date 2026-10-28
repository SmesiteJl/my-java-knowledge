# BeanFactoryPostProcessor и свой scope

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Как BeanFactoryPostProcessor меняет BeanDefinition до создания бинов: setInitMethodName по @PostConstruct, объявленной в интерфейсе
* Почему у бинов из Java-конфигурации getBeanClassName() возвращает null (factory method)
* @Autowired на методе с параметром как способ инъекции
* BeanFactoryPostProcessor, запрещающий prototype-бин с destroy-методом
* Свой Scope (бин живёт 2 секунды, кэш Guava) и регистрация через beanFactory.registerScope в BFPP
* @Scope(proxyMode = TARGET_CLASS): scoped-прокси для внедрения короткоживущего бина в синглтон
