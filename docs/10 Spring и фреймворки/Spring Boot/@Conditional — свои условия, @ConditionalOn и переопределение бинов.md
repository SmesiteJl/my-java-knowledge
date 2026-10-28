# @Conditional: свои условия, @ConditionalOn* и переопределение бинов

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Аннотация @Conditional и интерфейс Condition: метод matches(ConditionContext, AnnotatedTypeMetadata)
* Своя условная аннотация (@ConditionalOnProduction) поверх @Conditional
* Сколько раз вызывается Condition: над классом конфигурации, в стартере и над @Bean-методом
* Зачем кэшировать результат дорогого условия в статическом поле
* Обзор: @ConditionalOnBean/MissingBean, OnClass/MissingClass, OnProperty, OnWebApplication, OnResource, OnSingleCandidate и др.
* @ConditionalOnProperty: name, havingValue, matchIfMissing; почему её нельзя повторить с разными значениями
* Как @ConditionalOnClass читает аннотации, ссылающиеся на отсутствующие классы (ASM вместо рефлексии); почему лучше указывать имя класса строкой
* Композитные условия: AllNestedConditions и AnyNestedCondition, ConfigurationPhase.REGISTER_BEAN
* Как стартер уступает бину, объявленному в приложении (@ConditionalOnMissingBean)
* Чем конфликт двух бинов одного типа отличается от перезатирания бина с тем же именем
* Имя бина из @Bean-метода; отключение бина стартера своим бином с тем же id и риск при смене имени метода
