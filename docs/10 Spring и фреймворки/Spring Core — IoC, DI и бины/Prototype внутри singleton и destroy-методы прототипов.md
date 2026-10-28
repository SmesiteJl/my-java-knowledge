# Prototype внутри singleton и destroy-методы прототипов

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Prototype-бин, внедрённый в singleton, создаётся один раз: как получать новый prototype внутри singleton — @Lookup-метод, ObjectProvider/ObjectFactory, ApplicationContext.getBean, scoped proxy
* Почему @PreDestroy у prototype не вызывается при закрытии контекста; BPP-предупреждение по BeanDefinition.isPrototype()
