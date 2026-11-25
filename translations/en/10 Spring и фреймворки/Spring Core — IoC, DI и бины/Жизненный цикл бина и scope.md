# Bean lifecycle and scope

## First the recipe, then the bean

A bean is an object that Spring manages. For example, [we can declare `terminatorQuoter` in XML](XML-конфигурация,%20BeanDefinition%20и%20ClassPathXmlApplicationContext.md) by specifying a class and a value for the `message` property. When Spring has only read the declaration, we have a `BeanDefinition`, but no object yet.

When the factory needs to create a bean, it takes that recipe. It usually calls the constructor first, then populates the properties and runs initialization, with post-processors before and after it. The last two steps are easy to spot in [Spring's source code](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L606-L607): `populateBean()`, then `initializeBean()`.

In [`initializeBean()`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L1813-L1834), we get `postProcessBeforeInitialization()`, then the factory calls the init methods, and then comes `postProcessAfterInitialization()`. For instance, a post-processor can do some extra setup before `init()` and return a proxy instead of the original object afterward. That's the usual path, but it doesn't mean proxies can only show up there. The [article on `BeanPostProcessor`](BeanPostProcessor%20—%20свои%20аннотации%20и%20обработка%20бинов.md) goes into the details.

## Why have a separate init method when we already have a constructor?

Inside the `TerminatorQuoter` constructor, it's too early to read `message`: `<property>` calls the setter **after** the constructor. Without a default value, the field will be `null`, and calling `message.length()` right away will give us a `NullPointerException`. An `int` field in the same spot would be `0`, which is easy to mistake for a real value. [Those are Java's initial field values](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.12.5), not values Spring configured for us.

If we need the value in the constructor, we pass it [through constructor parameters](https://smesitejl.github.io/my-java-knowledge/ru/10%20Spring%20и%20фреймворки/Spring%20Core%20—%20IoC,%20DI%20и%20бины/Внедрение%20через%20конструктор/) (Russian). If our setup logic needs properties that have already been set, we move it to a separate init method. “Two-phase constructor” is just a handy name for those two steps: first the regular Java constructor, then a separate call from Spring after injection.

How do we set up the second step? In XML, put `init-method="init"` on `<bean>`. In Java configuration, we can use `@Bean(initMethod = "init")`. There's also `InitializingBean.afterPropertiesSet()` and `@PostConstruct`. The annotation takes effect during `postProcessBeforeInitialization()`, when `CommonAnnotationBeanPostProcessor` handles it. On shutdown, we have matching options: `destroy-method` in XML, `@Bean(destroyMethod = "cleanup")`, `DisposableBean.destroy()`, and `@PreDestroy`. The [Spring docs](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-nature.html#beans-factory-lifecycle-combined-effects) give the order for when we enable several mechanisms with different methods: the annotated method first, then the interface method, then the explicitly configured method.

**Init means this particular bean is ready.** If we need to wait for the whole context to finish refreshing, that's [a separate step with `ContextRefreshedEvent`](Трёхфазный%20конструктор%20—%20ContextRefreshedEvent%20и%20@PostInitialize.md).

## Who keeps the instances?

*Scope* determines when to create a fresh instance and when to return an existing one. With [`singleton`](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-scopes.html#beans-factory-scopes-singleton), the default scope, there's one shared instance per bean name within a given container. This isn't the Singleton pattern for the whole class: two definitions of the same class under different names can give us two objects. The factory keeps the finished singletons in a cache, separate from the definitions.

By default, `ApplicationContext` [creates non-lazy singletons up front during `refresh()`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-context/src/main/java/org/springframework/context/support/AbstractApplicationContext.java#L987). A [lazy bean](https://smesitejl.github.io/my-java-knowledge/ru/10%20Spring%20и%20фреймворки/Spring%20Core%20—%20IoC,%20DI%20и%20бины/Ленивые%20бины%20—%20@Lazy,%20lazyInit%20и%20@Primary/) (Russian) is usually created the first time we ask for it, but it can be needed earlier as a dependency of a singleton that's created at startup. If we just run the reader against an empty factory with no context, loading the definitions doesn't kick off early instantiation on its own.

With [`prototype`](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-scopes.html#beans-factory-scopes-prototype), the factory creates, configures, and hands out a new instance for every request. A request can be a direct `getBean()` call or the factory resolving a dependency. So if we [inject a prototype into a singleton once](https://smesitejl.github.io/my-java-knowledge/ru/10%20Spring%20и%20фреймворки/Spring%20Core%20—%20IoC,%20DI%20и%20бины/Prototype%20внутри%20singleton%20и%20destroy-методы%20прототипов/) (Russian), the reference we've stored won't start pointing to a new object on its own.

What does it mean when we say the factory “forgets” a prototype? The definition is still there, so it can make another bean just like it later. But the factory doesn't put the finished instance in the singleton cache or [register it for automatic destruction](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractBeanFactory.java#L1938-L1954). Whoever got the instance still has the same reference. If the prototype holds a resource, whoever uses it needs to release it. For singletons, when the context closes, the factory [runs the registered destruction callbacks and clears the cache](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/DefaultSingletonBeanRegistry.java#L696-L734). “No automatic destruction for prototypes” doesn't mean “only singletons get destroyed”: some other scopes manage their own cleanup.

## Checking the order with the same XML

Let's take the same three files from [the `TerminatorQuoter` example](XML-конфигурация,%20BeanDefinition%20и%20ClassPathXmlApplicationContext.md) and stick with Java 21 and Spring 6.2.11. We'll add a constructor and two methods to `TerminatorQuoter` to see which one first sees the value of `message`. We'll leave the setter and `sayQuote()` alone.

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

In `context.xml`, replace the `terminatorQuoter` declaration with two beans of the same class:

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

In `Main.java`, replace the body of `main()`. Before running, use the IDE to add the imports for `ClassPathXmlApplicationContext` from `org.springframework.context.support` and `TerminatorQuoter` from `quoters`.

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

Expected output:

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

The singleton already exists by the time we print `ready`. We ask for it twice and get the same object (`true`). But two requests for the prototype give us two different objects (`false`). In all three cases, the constructor prints `null`, while `init()` already sees the value from the XML. When we close the context, `cleanup()` runs only for the singleton.

> [!QUESTION]- Check yourself
> - How does `BeanFactory` use `BeanDefinition`, and where does it keep singletons?
> - What happens before and after init, and when can a post-processor return a proxy?
> - Why can't the constructor read a value Spring sets through a setter?
> - How do we configure initialization and destruction callbacks?
> - When are `singleton` and `prototype` beans created, and why isn't `prototype` destruction automatic?

## References

* [Eugene Borisov, “Spring the Ripper”: why init comes after the constructor](https://www.youtube.com/watch?v=BmBr5diz8WA&t=1135s) — the talk on video.
* [“Spring the Ripper” on the JUG Ru Group blog](https://habr.com/ru/companies/jugru/articles/893638/) — the sections “How it all works” and “Init methods and the two-phase constructor.”
* [Spring Reference: Bean scopes](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-scopes.html) — singleton, prototype, and other scopes.
* [Spring Reference: Lifecycle callbacks](https://docs.spring.io/spring-framework/reference/6.2/core/beans/factory-nature.html#beans-factory-lifecycle-combined-effects) — which mechanisms are available and what order they run in.
* [`AbstractAutowireCapableBeanFactory`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L1813-L1834), [`AbstractApplicationContext`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-context/src/main/java/org/springframework/context/support/AbstractApplicationContext.java#L987), and [`AbstractBeanFactory`](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractBeanFactory.java#L1938-L1954) — initialization, pre-instantiation, and cleanup registration in Spring 6.2.11.
* [`AbstractAutowireCapableBeanFactory`: Populating properties and initialization](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L606-L607) and [`DefaultSingletonBeanRegistry`: Shutdown](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/DefaultSingletonBeanRegistry.java#L696-L734) — the order of operations and cache cleanup.
* [JLS 4.12.5: Initial values of variables](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.12.5) — where `null` and `0` come from before injection.
