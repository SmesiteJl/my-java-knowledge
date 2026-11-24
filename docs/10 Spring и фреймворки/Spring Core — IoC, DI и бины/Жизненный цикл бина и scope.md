# Жизненный цикл бина и scope

## Сначала рецепт, потом бин

Бин — объект, которым управляет Spring. Например, [в XML можно объявить `terminatorQuoter`](XML-конфигурация,%20BeanDefinition%20и%20ClassPathXmlApplicationContext.md): указать класс и значение свойства `message`. Пока Spring прочитал только декларацию, у нас есть `BeanDefinition`, но объекта ещё нет.

Когда бин нужен, `BeanFactory` создаёт экземпляр по этому описанию. В обычном случае она вызывает конструктор, заполняет свойства, прогоняет объект через обработчики до и после инициализации и отдаёт результат. В [исходнике Spring](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L606-L607) это хорошо видно по двум вызовам подряд: `populateBean()`, затем `initializeBean()`.

В [`initializeBean()`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L1813-L1834) идут `postProcessBeforeInitialization()`, вызов init-методов фабрикой и `postProcessAfterInitialization()`. Например, обработчик может выполнить дополнительную настройку перед `init()`, а после него вернуть прокси вместо исходного объекта. Это обычный путь, а не обещание, что прокси всегда появляется только здесь: подробности — в [статье про `BeanPostProcessor`](BeanPostProcessor%20—%20свои%20аннотации%20и%20обработка%20бинов.md).

## Зачем отдельный init, если есть конструктор

В конструкторе `TerminatorQuoter` ещё рано читать `message`: `<property>` вызывает сеттер **после** конструктора. Без значения по умолчанию поле будет `null`, и, если сразу вызвать `message.length()`, словим `NullPointerException`. У поля типа `int` в такой же ситуации будет `0`, который легко принять за настоящее значение. [Это начальные значения полей в Java](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.12.5), а не то, что нам настроил Spring.

Если значение нужно уже в конструкторе, передаём его [через параметры конструктора](Внедрение%20через%20конструктор.md). Если же логике настройки нужны уже заполненные сеттерами свойства, выносим её в отдельный init-метод. «Двухфазовый конструктор» здесь — удобное название для двух этапов: сначала обычный Java-конструктор, потом, после внедрения, отдельный вызов Spring.

Как задать второй этап? В XML на `<bean>` ставим `init-method="init"`, в Java-конфигурации можно указать `@Bean(initMethod = "init")`. Есть ещё `InitializingBean.afterPropertiesSet()` и `@PostConstruct`. Аннотация срабатывает в фазе `postProcessBeforeInitialization()`, когда её обрабатывает `CommonAnnotationBeanPostProcessor`. Для закрытия есть симметричные варианты: `destroy-method` в XML, `@Bean(destroyMethod = "cleanup")`, `DisposableBean.destroy()` и `@PreDestroy`. В [документации Spring](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-nature.html#beans-factory-lifecycle-combined-effects) указан порядок, если методы разные и мы включили сразу несколько механизмов: сначала аннотация, затем метод интерфейса, затем явно заданный метод.

**Init — это готовность конкретного бина.** Если задача требует дождаться обновления всего контекста, это уже [отдельный этап с `ContextRefreshedEvent`](Трёхфазный%20конструктор%20—%20ContextRefreshedEvent%20и%20@PostInitialize.md).

## Кто хранит экземпляры

*Scope* определяет, когда создавать новый экземпляр и когда отдавать уже существующий. У [`singleton`](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-scopes.html#beans-factory-scopes-singleton), области видимости по умолчанию, один общий экземпляр на имя бина в пределах конкретного контейнера. Это не паттерн Singleton на весь класс: два определения одного класса под разными именами могут дать два объекта. Фабрика хранит готовые синглтоны в кэше, отдельно от определений.

По умолчанию `ApplicationContext` при [`refresh()` заранее создаёт синглтоны без ленивой инициализации](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-context/src/main/java/org/springframework/context/support/AbstractApplicationContext.java#L987). [Ленивый бин](Ленивые%20бины%20—%20@Lazy,%20lazyInit%20и%20@Primary.md) обычно создаётся при первом обращении, но может понадобиться раньше как зависимость синглтона, который создаётся при старте. Если же мы просто вызвали ридер на пустой фабрике без контекста, загрузка определений сама по себе не запускает предварительное создание.

С [`prototype`](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-scopes.html#beans-factory-scopes-prototype) при каждом новом запросе фабрика создаёт, настраивает и отдаёт новый экземпляр. Запрос — это и прямой `getBean()`, и разрешение зависимости. Поэтому, если мы [один раз внедрили прототип в синглтон](Prototype%20внутри%20singleton%20и%20destroy-методы%20прототипов.md), уже сохранённая ссылка не станет сама указывать на новый объект.

Что значит «фабрика забыла прототип»? Определение осталось: по нему потом можно сделать ещё один такой бин. А готовый экземпляр фабрика не кладёт в кэш синглтонов и [не регистрирует для автоматического вызова destroy](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractBeanFactory.java#L1938-L1954). Ссылка у получателя как была, так и осталась. Если прототип держит ресурс, освобождать его должен тот, кто им пользуется. Для синглтонов при закрытии контекста фабрика [вызывает зарегистрированные колбэки уничтожения и очищает кэш](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/DefaultSingletonBeanRegistry.java#L696-L734). Правило «нет автоматического destroy у прототипа» не означает «destroy бывает только у синглтона»: некоторые другие области видимости управляют очисткой сами.

## Проверяем порядок на том же XML

Учебное продолжение [примера с `TerminatorQuoter`](XML-конфигурация,%20BeanDefinition%20и%20ClassPathXmlApplicationContext.md): используем те же Java 21, Spring 6.2.11 и три файла. В `TerminatorQuoter.java` внутри класса добавим конструктор и два метода. Сеттер и `sayQuote()` оставим как есть.

```java
public TerminatorQuoter() {
    System.out.println("constructor: " + message);
}

public void init() {
    System.out.println("init: " + message);
}

public void cleanup() {
    System.out.println("cleanup: " + message);
}
```

В `context.xml` заменим декларацию `terminatorQuoter` двумя бинами того же класса:

```xml
<bean id="singletonQuoter" class="quoters.TerminatorQuoter"
      init-method="init" destroy-method="cleanup">
    <property name="message" value="singleton"/>
</bean>
<bean id="prototypeQuoter" class="quoters.TerminatorQuoter" scope="prototype"
      init-method="init" destroy-method="cleanup">
    <property name="message" value="prototype"/>
</bean>
```

В `Main.java` заменим тело `main()`:

```java
System.out.println("open");
try (var context = new ClassPathXmlApplicationContext("context.xml")) {
    System.out.println("ready");
    var first = context.getBean("singletonQuoter", TerminatorQuoter.class);
    var second = context.getBean("singletonQuoter", TerminatorQuoter.class);
    System.out.println(first == second);
    var third = context.getBean("prototypeQuoter", TerminatorQuoter.class);
    var fourth = context.getBean("prototypeQuoter", TerminatorQuoter.class);
    System.out.println(third == fourth);
}
```

Ожидаемый вывод:

```text
open
constructor: null
init: singleton
ready
true
constructor: null
init: prototype
constructor: null
init: prototype
false
cleanup: singleton
```

До `ready` фабрика уже создала синглтон. Конструкторы ещё не видят свойство, а `init()` видит его у каждого экземпляра. При закрытии контекста `cleanup()` автоматически отработал только для синглтона из этого примера.

> [!QUESTION]- Проверь себя
> - Как `BeanFactory` использует `BeanDefinition` и где хранит синглтоны?
> - Что происходит до и после init, когда обработчик может вернуть прокси?
> - Почему в конструкторе нельзя прочитать значение, которое Spring задаёт через сеттер?
> - Как задать колбэки инициализации и уничтожения?
> - Когда создаются `singleton` и `prototype` и почему у `prototype` нет автоматического destroy?

## Ссылки

* [Евгений Борисов, «Spring-потрошитель»: зачем init после конструктора](https://www.youtube.com/watch?v=BmBr5diz8WA&t=1135s) — видео доклада.
* [«Spring-потрошитель» в блоге JUG Ru Group](https://habr.com/ru/companies/jugru/articles/893638/) — разделы «Как всё работает» и «Init-методы и двухфазный конструктор».
* [Spring Reference: Scope бинов](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-scopes.html) — синглтон, прототип и другие области видимости.
* [Spring Reference: Колбэки жизненного цикла](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-nature.html#beans-factory-lifecycle-combined-effects) — механизмы и порядок вызова.
* [`AbstractAutowireCapableBeanFactory`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L1813-L1834), [`AbstractApplicationContext`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-context/src/main/java/org/springframework/context/support/AbstractApplicationContext.java#L987) и [`AbstractBeanFactory`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractBeanFactory.java#L1938-L1954) — инициализация, предварительное создание и регистрация очистки в Spring 6.2.11.
* [`AbstractAutowireCapableBeanFactory`: заполнение свойств и инициализация](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L606-L607) и [`DefaultSingletonBeanRegistry`: закрытие](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/DefaultSingletonBeanRegistry.java#L696-L734) — очерёдность шагов и очистка кэша.
* [JLS 4.12.5: начальные значения переменных](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.12.5) — откуда берутся `null` и `0` до внедрения.

