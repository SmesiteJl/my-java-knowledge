# BeanPostProcessor: Custom Annotations and Bean Processing

## The random number comes after the constructor

We put `@InjectRandomInt(min = 2, max = 7)` on the `repeat` field of the quoter from [Evgeny Borisov's “Spring Ripper” talk (10:06)](https://www.youtube.com/watch?v=BmBr5diz8WA&t=606s). The field tells us how many times to print the quote. If we create the object with `new` and call `sayQuote()` right away, nothing gets printed: the annotation doesn't write anything on its own, and `repeat` is still `0`.

So where do we set the number? We could do it in the constructor, but then the quoter would be responsible for both picking the number and printing the quote. In this example, Java creates the object, Spring fills it in, and then we check the value in `init()`. That's what's meant here by a [*two-phase constructor* (18:55)](https://www.youtube.com/watch?v=BmBr5diz8WA&t=1135s): one Java constructor, then a separate initialization step after configuration. If we can't create a valid object without the value, we're better off passing it to the constructor.

### Between creation and `init()`

[`BeanPostProcessor`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/config/BeanPostProcessor.html) (BPP) is a container extension point that works on bean instances rather than `BeanDefinition` metadata. In the usual [bean lifecycle](Жизненный%20цикл%20бина%20и%20scope.md), Spring creates the object, injects dependencies and sets properties, runs the `postProcessBeforeInitialization()` chain, calls `afterPropertiesSet()` and/or the configured `init` method, and then runs `postProcessAfterInitialization()`.

[`@PostConstruct`](https://docs.spring.io/spring-framework/reference/core/beans/factory-nature.html#beans-factory-lifecycle-combined-effects) is a little different: `CommonAnnotationBeanPostProcessor` calls it **inside the before chain**. So it's not enough to say, “I'm writing the value in the before phase, so I'll definitely beat `@PostConstruct`.” Our processor has to run ahead of that one. `@Autowired` is a different story: `AutowiredAnnotationBeanPostProcessor` resolves dependencies from the container. For a field, it does that during property population, through `postProcessProperties()`. Our processor doesn't ask the container for a value; it generates the number itself.

The chain is like *Chain of Responsibility*: each processor gets the result of the previous one. In either phase, we can return the same bean or a wrapper. If we return `null`, Spring [stops the current chain and keeps the last non-null result](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L423-L451). So “no annotation, nothing to do” means `return bean`, not `return null`. For autodetected BPPs, `PriorityOrdered` and `Ordered` control the order. For processors added through `addBeanPostProcessor()`, registration order wins.

### Declaring the annotation and writing the processor

In our example, `@Retention(RetentionPolicy.RUNTIME)` keeps the annotation available at runtime, and `@Target(ElementType.FIELD)` lets us put it only on fields. The processor finds those fields and writes a number before `init()` runs.

```java
public class Demo {
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.FIELD)
    @interface InjectRandomInt {
        int min();
        int max(); // the upper bound is exclusive
    }

    static final class InjectRandomIntAnnotationBeanPostProcessor
            implements BeanPostProcessor, PriorityOrdered {
        @Override
        public int getOrder() {
            return HIGHEST_PRECEDENCE; // run before the processor that handles @PostConstruct
        }

        @Override
        public Object postProcessBeforeInitialization(Object bean, String beanName) {
            for (var field : bean.getClass().getDeclaredFields()) {
                var annotation = field.getAnnotation(InjectRandomInt.class);
                if (annotation == null) {
                    continue;
                }
                int modifiers = field.getModifiers();
                if (field.getType() != int.class
                        || Modifier.isStatic(modifiers) || Modifier.isFinal(modifiers)) {
                    throw new IllegalArgumentException("@InjectRandomInt: " + field);
                }
                int value = ThreadLocalRandom.current()
                        .nextInt(annotation.min(), annotation.max());
                ReflectionUtils.makeAccessible(field);
                ReflectionUtils.setField(field, bean, value);
            }
            return bean;
        }
    }
```

We use [reflection](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/Аннотации%20и%20рефлексия/Рефлексия%20и%20класс%20Class/) (Russian) to get the fields declared directly on the class: `getDeclaredFields()` sees `private` fields, but not fields declared by superclasses. To write to a `private` field, we make it accessible through reflection and then call [`ReflectionUtils.setField()`](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/util/ReflectionUtils.html#setField(java.lang.reflect.Field,java.lang.Object,java.lang.Object)). We only change non-static `int` fields that aren't `final`.

With [`ThreadLocalRandom.current().nextInt(min, max)`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ThreadLocalRandom.html#nextInt(int,int)), we don't have to create a `new Random()` for every field. It includes the lower bound, excludes the upper bound, and throws `IllegalArgumentException` if `min >= max`. So with `min = 2, max = 7`, we can get **2–6**, but not 7. Our `init()` checks that instead of just assuming it.

## After `init()`, we can return a proxy

[Profiling (25:57)](https://www.youtube.com/watch?v=BmBr5diz8WA&t=1557s) is a different job: instead of changing a field, we want to time calls to methods on a bean marked with `@Profiling`. We don't rewrite the bean class. After initialization, we return a *proxy*: a separate object that receives the call, delegates it to the bean, and prints the elapsed time when the flag is on. That way `init()` runs on the populated object before our processor swaps in the wrapper.

Here's the gotcha: in `postProcessAfterInitialization()`, we might already be looking at another processor's result. On a JDK proxy, `getClass()` returns the proxy class, so it's too late to look there for the annotation on the implementation. In the before phase, while we still have the original in our example, we save `beanName → Class<?>`. In the after phase, we look up the entry by the same `beanName`. The object changed, but the name Spring uses to pass this bean through the chain didn't. We read metadata from the class we saved, but delegate the call to **the object we got in the after phase** so we don't throw away wrappers that are already in place. This trick doesn't guarantee we'll get the original in the before phase: if something has already swapped out the object, we'll need somewhere else to read the metadata.

A question I had:

> *How does the bean know its own interfaces? I get the class loader, but where do the interfaces come from?*

The bean doesn't store a list of interfaces in its fields. `getClass()` gives us a `Class` object, and [`Class.getInterfaces()`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Class.html#getInterfaces()) reads the interfaces the class implements **directly** from its metadata. For our class, that's `Quoter`. We pass those interfaces and the original class's loader to [`Proxy.newProxyInstance()`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/Proxy.html#newProxyInstance(java.lang.ClassLoader,java.lang.Class%5B%5D,java.lang.reflect.InvocationHandler)). The proxy will be defined in that loader, which needs to see the exact same interface types, not just classes with the same names.

That's why we can use a JDK proxy as a `Quoter` but can't cast it to `TerminatorQuoter`. [A CGLIB proxy in Spring](https://smesitejl.github.io/my-java-knowledge/ru/10%20Spring%20и%20фреймворки/АОП/Прокси%20в%20Spring%20—%20JDK%20Dynamic%20Proxy%20и%20CGLIB/) (Russian) works differently: it creates a subclass, so it works when we need the implementation type, but it can't extend a `final` class or override a `final` method. Either way, the call has to go through the proxy. If the target object calls one of its own methods through `this`, [the wrapper won't see it](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html).

### Timing and a switch in the same process

[JMX](https://smesitejl.github.io/my-java-knowledge/ru/04%20JVM%20и%20производительность/Мониторинг%20и%20диагностика%20JVM/JMX%20—%20MBean%20и%20MBeanServer/) (Russian), or *Java Management Extensions*, is a Java API for monitoring and management. An *MBean* is an object that exposes its management interface through that API. It doesn't have to be a Spring bean. We register the controller with the platform `MBeanServer` under the name `profiling:name=controller`. The `isEnabled()` / `setEnabled()` pair becomes a readable and writable JMX attribute called `Enabled`. The usual Standard MBean naming convention pairs a `ProfilingController` class with a `ProfilingControllerMBean` interface. In the example, we pair them explicitly with [`StandardMBean`](https://docs.oracle.com/en/java/javase/25/docs/api/java.management/javax/management/StandardMBean.html).

The flag is `volatile` because JMX changes it from another thread: [a subsequent read sees the write](https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html#jls-17.4.5). We check the flag once, at the start of the call, so flipping it doesn't cancel a measurement that's already underway. This isn't [Spring profiles and `@Profile`](https://smesitejl.github.io/my-java-knowledge/ru/10%20Spring%20и%20фреймворки/Spring%20Boot/Профили%20и%20@Profile/) (Russian): the bean is already there, the proxy stays the same, and only its behavior on subsequent calls changes.

Now we can add the profiling processor. One singleton bean that directly implements the public `Quoter` interface is enough to see what happens in the before phase and what happens in the after phase. We're not using this code to replace Spring AOP.

```java
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.TYPE)
    @interface Profiling {}

    public interface ProfilingControllerMBean {
        boolean isEnabled();
        void setEnabled(boolean enabled);
    }

    public static final class ProfilingController implements ProfilingControllerMBean {
        private volatile boolean enabled;

        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
    }

    static final class ProfilingPostProcessor implements BeanPostProcessor {
        private final Map<String, Class<?>> originals = new HashMap<>();
        private final ProfilingController controller = new ProfilingController();

        @Override
        public Object postProcessBeforeInitialization(Object bean, String beanName) {
            Class<?> type = bean.getClass();
            if (type.isAnnotationPresent(Profiling.class)) {
                originals.put(beanName, type);
            }
            return bean;
        }

        @Override
        public Object postProcessAfterInitialization(Object bean, String beanName) {
            Class<?> original = originals.remove(beanName);
            if (original == null) {
                return bean;
            }
            return Proxy.newProxyInstance(original.getClassLoader(), original.getInterfaces(),
                    (proxy, method, args) -> {
                        // the wrapper itself uses reference equality; we don't time these methods
                        if (method.getDeclaringClass() == Object.class) {
                            return switch (method.getName()) {
                                case "equals" -> proxy == args[0];
                                case "hashCode" -> System.identityHashCode(proxy);
                                case "toString" -> "Прокси бина " + beanName;
                                default -> throw new AssertionError(method);
                            };
                        }
                        boolean measure = controller.isEnabled();
                        long start = measure ? System.nanoTime() : 0;
                        try {
                            return method.invoke(bean, args);
                        } catch (InvocationTargetException ex) {
                            throw ex.getCause();
                        } finally {
                            if (measure) {
                                System.out.printf("%s.%s: %d нс%n", beanName,
                                        method.getName(), System.nanoTime() - start);
                            }
                        }
                    });
        }
    }
```

Notice that we don't need a wall clock to measure elapsed time. By the contract of [`System.nanoTime()`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/System.html#nanoTime()), the difference between two readings is meaningful, not the reading itself. `finally` prints the time even if the call throws, and we pull the original cause out of [`InvocationTargetException`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/InvocationTargetException.html#getCause()) so the caller doesn't get reflection's exception wrapper. The timing includes reflective delegation: we're observing a call, not running a microbenchmark.

### Putting the example together and flipping the flag

We still need to register both processors. The [JUG Ru write-up of the talk](https://habr.com/ru/companies/jugru/articles/893638/) uses XML for this: `<bean class="quoters.InjectRandomIntAnnotationBeanPostProcessor"/>`. We don't need an explicit `id`: Spring gives the bean a name and finds the processor by type. In XML, we turn on processing for standard annotations separately, for example with `<context:annotation-config/>`.

We declare both processors with `static @Bean` methods whose signatures use the concrete return types. That lets Spring identify the processors early and create them without instantiating the configuration class too soon.

```java
    public interface Quoter {
        void sayQuote();
    }

    @Profiling
    static final class TerminatorQuoter implements Quoter {
        @InjectRandomInt(min = 2, max = 7)
        private int repeat;

        TerminatorQuoter() {
            System.out.println("Конструктор: repeat = " + repeat); // 0
        }

        @PostConstruct
        void init() {
            if (repeat < 2 || repeat > 6) {
                throw new IllegalStateException("Ожидалось число от 2 до 6: " + repeat);
            }
            System.out.println("init: repeat = " + repeat);
        }

        public void sayQuote() {
            for (int i = 0; i < repeat; i++) {
                System.out.println("I'll be back");
            }
        }
    }

    @Configuration(proxyBeanMethods = false)
    static class Config {
        @Bean
        static InjectRandomIntAnnotationBeanPostProcessor randomIntProcessor() {
            return new InjectRandomIntAnnotationBeanPostProcessor();
        }

        @Bean
        static ProfilingPostProcessor profilingProcessor() {
            return new ProfilingPostProcessor();
        }

        @Bean
        Quoter terminatorQuoter() {
            return new TerminatorQuoter();
        }
    }

    public static void main(String[] args) throws Exception {
        try (var context = new AnnotationConfigApplicationContext(Config.class);
             var input = new BufferedReader(new InputStreamReader(System.in))) {
            var quoter = context.getBean("terminatorQuoter", Quoter.class);
            var processor = context.getBean(ProfilingPostProcessor.class);
            var server = ManagementFactory.getPlatformMBeanServer();
            var name = new ObjectName("profiling:name=controller");
            server.registerMBean(
                    new StandardMBean(processor.controller, ProfilingControllerMBean.class), name);
            try {
                System.out.println("JVM pid: " + ProcessHandle.current().pid());
                System.out.println("Enter — вызов sayQuote(); q — выход");
                for (String line; (line = input.readLine()) != null && !line.equals("q"); ) {
                    quoter.sayQuote();
                }
            } finally {
                server.unregisterMBean(name);
            }
        }
    }
}
```

To run the example, paste the three Java blocks in order into `Demo.java` and add the omitted imports. With Spring 6.2, we use `@PostConstruct` from `jakarta.annotation`, not `javax.annotation`. The JMX classes `ObjectName` and `StandardMBean` are still in the JDK's `javax.management` package.

We need Maven and JDK 25. Save `pom.xml` next to `Demo.java`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>demo</groupId>
  <artifactId>bean-post-processor</artifactId>
  <version>1.0</version>
  <dependencies>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>6.2.11</version>
    </dependency>
    <dependency>
      <groupId>jakarta.annotation</groupId>
      <artifactId>jakarta.annotation-api</artifactId>
      <version>2.1.1</version>
    </dependency>
  </dependencies>
</project>
```

```bash
mvn -q org.apache.maven.plugins:maven-dependency-plugin:3.8.1:copy-dependencies
java -cp 'target/dependency/*' Demo.java
```

In the constructor we'll see `0`; in `init()` we'll see a number from 2 to 6. Press Enter: the app prints the quotes without timing the call. Then start `jconsole` in another terminal and select the JVM by its printed PID under **Local Process**. Under **MBeans → profiling → controller → Attributes**, set `Enabled` to `true`. Press Enter again in the app's terminal: after the quotes, you'll see `terminatorQuoter.sayQuote: … нс` (`нс` means nanoseconds). Set it back to `false` and the next call won't be timed. We didn't recreate the bean, the proxy, or the context.

It's easy to mishear this part: they're talking about a JMX console, not Consul. [In the talk (45:57)](https://www.youtube.com/watch?v=BmBr5diz8WA&t=2757s), Borisov flips the switch in Java VisualVM with the MBeans plugin; we're using [JConsole from the JDK](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jconsole.html). For a local connection under the same user account, we don't need a remote port or any remote JMX configuration.

## The takeaway

In the constructor, we still have `0`; in `init()`, we have `2–6`; and we only see timing for a call through the proxy with the flag on. **Here's the rule:** if we need to get the bean itself ready for `init()`, do it in the before phase and watch the processor order. If we need to intercept future calls, return a proxy in the after phase.

What if we need to call a method *through the proxy* once the context is ready? `@PostConstruct` alone won't do it. That's what the [article on `ContextRefreshedEvent` and `@PostInitialize`](Трёхфазный%20конструктор%20—%20ContextRefreshedEvent%20и%20@PostInitialize.md) covers.

> [!QUESTION]- Test yourself: interview questions covered in this article
> - How does the `BeanPostProcessor` chain work, and what does returning `null` mean?
> - Where do the before and after phases sit in the lifecycle, and why do we usually return a proxy from the after phase?
> - How do we register a processor and write a number to a `private` field before `init()`?
> - What handles `@Autowired` and `@PostConstruct`, and why does BPP order matter?
> - Why save a bean's name and class before wrapping it? What do we pass in to create a JDK proxy?
> - How do we time a call without losing the original exception, and how do we toggle timing on the fly through JMX?

## Sources

* [Evgeny Borisov, “Spring Ripper”](https://www.youtube.com/watch?v=BmBr5diz8WA) — the original talk.
* [JUG Ru's write-up of the talk](https://habr.com/ru/companies/jugru/articles/893638/) — the original example with XML, the quoter, and JMX.
* [Spring Framework: BeanPostProcessor](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/config/BeanPostProcessor.html) — the contract, ordering, and registration of processors.
* [Spring Framework: Combining lifecycle mechanisms](https://docs.spring.io/spring-framework/reference/core/beans/factory-nature.html#beans-factory-lifecycle-combined-effects) — the order of `@PostConstruct`, `afterPropertiesSet()`, and a custom `init` method.
* [Spring 6.2.11 source: the before and after chains](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L423-L451) — how each processor gets the previous one's result.
* [Spring Framework: ReflectionUtils.setField()](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/util/ReflectionUtils.html#setField(java.lang.reflect.Field,java.lang.Object,java.lang.Object)) — writing to a field through reflection.
* [Spring Framework: AOP proxies](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html) — how JDK dynamic proxies differ from CGLIB proxies and why calls through `this` don't go through the proxy.
* [JDK: ThreadLocalRandom.nextInt()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ThreadLocalRandom.html#nextInt(int,int)) — the bounds of the range.
* [JDK: Class.getInterfaces()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Class.html#getInterfaces()) and [Proxy.newProxyInstance()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/Proxy.html#newProxyInstance(java.lang.ClassLoader,java.lang.Class%5B%5D,java.lang.reflect.InvocationHandler)) — where the interfaces come from and how a JDK proxy is created.
* [JDK: System.nanoTime()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/System.html#nanoTime()) and [InvocationTargetException.getCause()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/InvocationTargetException.html#getCause()) — measuring elapsed time and retrieving the original exception.
* [JLS §17.4.5](https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html#jls-17.4.5) — visibility of a `volatile` write across threads.
* [JDK: StandardMBean](https://docs.oracle.com/en/java/javase/25/docs/api/java.management/javax/management/StandardMBean.html) and [JConsole](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jconsole.html) — the management interface and local connections.
