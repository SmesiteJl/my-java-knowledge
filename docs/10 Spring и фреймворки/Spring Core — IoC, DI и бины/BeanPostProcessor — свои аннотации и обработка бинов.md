# BeanPostProcessor: свои аннотации и обработка бинов

## Случайное число появляется после конструктора

У кворера из [доклада Евгения Борисова «Spring-потрошитель» (10:06)](https://www.youtube.com/watch?v=BmBr5diz8WA&t=606s) есть поле `repeat`: сколько раз печатать цитату. Мы пишем над ним `@InjectRandomInt(min = 2, max = 7)`. Вызываем метод — и без обработчика не печатается ни одной цитаты. Аннотация — просто метаданные, а поле `int` по-прежнему равно `0`.

Можно было бы посчитать число в конструкторе. Но тогда сам кворер отвечал бы и за выбор значения, и за то, что с ним делать. В примере эти задачи разделены: сначала Java создаёт объект, затем Spring заполняет его и вызывает `init()`. Вот что здесь называется [*двухфазным конструктором* (18:55)](https://www.youtube.com/watch?v=BmBr5diz8WA&t=1135s): обычный конструктор и отдельная инициализация после настройки, а не два конструктора Java. Если значение необходимо для инварианта уже при создании объекта, лучше передать его конструктору.

### Между созданием и `init()`

[`BeanPostProcessor`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/config/BeanPostProcessor.html) (BPP) — точка расширения контейнера, которая работает с экземплярами бинов, а не с описаниями `BeanDefinition`. В обычном [жизненном цикле бина](Жизненный%20цикл%20бина%20и%20scope.md) Spring создаёт объект, заполняет зависимости и свойства, прогоняет цепочку `postProcessBeforeInitialization()`, вызывает `afterPropertiesSet()` и/или настроенный `init`-метод, затем прогоняет `postProcessAfterInitialization()`.

[`@PostConstruct`](https://docs.spring.io/spring-framework/reference/core/beans/factory-nature.html#beans-factory-lifecycle-combined-effects) здесь стоит особняком: его вызывает `CommonAnnotationBeanPostProcessor` **внутри before-цепочки**. То есть недостаточно сказать «я пишу в before, поэтому точно успею до `@PostConstruct`». Наш обработчик должен стоять раньше него. А `@Autowired` — другая история: `AutowiredAnnotationBeanPostProcessor` разрешает зависимости из контейнера; для поля он делает это на этапе заполнения свойств, через `postProcessProperties()`. Наш обработчик к контейнеру за значением не обращается, он сам генерирует число.

Цепочка похожа на *Chain of Responsibility*: каждый обработчик получает результат предыдущего. В обеих фазах можно вернуть тот же бин или обёртку; если вернуть `null`, Spring [остановит текущую цепочку и оставит последний ненулевой результат](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L423-L451). Поэтому «аннотации нет, ничего не делаем» — это `return bean`, а не `return null`. Для найденных автоматически BPP порядок задают `PriorityOrdered` и `Ordered`; для добавленных через `addBeanPostProcessor()` работает порядок регистрации.

### Объявляем аннотацию и регистрируем обработчик

В [текстовой версии доклада JUG Ru](https://habr.com/ru/companies/jugru/articles/893638/) обработчик объявлен в XML как `<bean class="quoters.InjectRandomIntAnnotationBeanPostProcessor"/>`. Явный `id` не нужен: контекст обнаруживает обработчики по типу, а для такой XML-записи Spring сгенерирует имя. Но просто написать класс обработчика и оставить его вне контекста недостаточно. Отдельно в XML нужно включить обработку стандартных аннотаций, например через `<context:annotation-config/>`; сам по себе XML её не включает.

Ниже **учебная адаптация**, не код из доклада. Соберём три Java-блока подряд в один файл `Demo.java`. Первый блок открывает класс `Demo`. Аннотация остаётся доступной в рантайме благодаря `@Retention(RetentionPolicy.RUNTIME)`, а `@Target(ElementType.FIELD)` ограничивает её полями.

```java
import jakarta.annotation.PostConstruct;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.management.ManagementFactory;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Modifier;
import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;
import javax.management.ObjectName;
import javax.management.StandardMBean;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.PriorityOrdered;
import org.springframework.util.ReflectionUtils;

public class Demo {
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.FIELD)
    @interface InjectRandomInt {
        int min();
        int max(); // верхняя граница не включается
    }

    static final class InjectRandomIntAnnotationBeanPostProcessor
            implements BeanPostProcessor, PriorityOrdered {
        @Override
        public int getOrder() {
            return HIGHEST_PRECEDENCE; // успеваем до обработчика @PostConstruct
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

Через [рефлексию](../../03%20Java%20Core/Аннотации%20и%20рефлексия/Рефлексия%20и%20класс%20Class.md) берём поля, объявленные непосредственно в классе: `getDeclaredFields()` видит `private`, но не поля родителей. Чтобы записать значение в `private`-поле, открываем к нему рефлексивный доступ, затем вызываем [`ReflectionUtils.setField()`](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/util/ReflectionUtils.html#setField(java.lang.reflect.Field,java.lang.Object,java.lang.Object)). Изменяем только нестатические поля `int` без `final`.

[`ThreadLocalRandom.current().nextInt(min, max)`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ThreadLocalRandom.html#nextInt(int,int)) не требует создавать `new Random()` на каждое поле. Он включает нижнюю границу, исключает верхнюю и бросает `IllegalArgumentException`, если `min >= max`. То есть при `min = 2, max = 7` возможны **2–6**, но не 7. В нашем `init()` это проверяется, а не просто предполагается.

## После `init()` можно вернуть прокси

Задача с [профилированием (25:57)](https://www.youtube.com/watch?v=BmBr5diz8WA&t=1557s) другая: мы не меняем поле, а хотим замерять вызовы методов бина, отмеченного `@Profiling`. Класс бина не переписываем. После инициализации возвращаем *прокси* — отдельный объект, который принимает вызов, делегирует его бину и при включённом флаге печатает время. Так `init()` успевает отработать на уже заполненном объекте до того, как наш обработчик подставит обёртку.

Засада: в `postProcessAfterInitialization()` перед нами может быть уже результат другого обработчика. У JDK-прокси `getClass()` вернёт класс прокси, и искать на нём метку реализации поздно. В before-фазе, пока в нашем примере виден оригинал, запоминаем `beanName → Class<?>`; в after-фазе находим запись по тому же `beanName`. Поменялся объект, но не имя, под которым Spring проводит этот бин через цепочку. Метаданные берём у сохранённого класса, а вызов делегируем **объекту, который получили в after**, чтобы не выбросить уже установленные обёртки. Сам приём не гарантирует оригинал в before: если кто-то подменил объект ещё раньше, потребуется другое место для чтения метаданных.

Вопрос, который у меня возник:

> *Почему бин знает свои интерфейсы? С загрузчиком понятно, а интерфейсы откуда?*

У бина нет списка интерфейсов в полях. `getClass()` даёт объект `Class`, а [`Class.getInterfaces()`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Class.html#getInterfaces()) читает из метаданных класса интерфейсы, которые он реализует **непосредственно**. Для нашего класса это `Quoter`. В [`Proxy.newProxyInstance()`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/Proxy.html#newProxyInstance(java.lang.ClassLoader,java.lang.Class%5B%5D,java.lang.reflect.InvocationHandler)) передаём эти интерфейсы и загрузчик оригинального класса: прокси будет определён в этом загрузчике, и ему должны быть видны те же типы интерфейсов, а не просто классы с такими же именами.

Поэтому JDK-прокси можно использовать как `Quoter`, но нельзя привести к `TerminatorQuoter`. [CGLIB-прокси в Spring](../АОП/Прокси%20в%20Spring%20—%20JDK%20Dynamic%20Proxy%20и%20CGLIB.md) устроен иначе: создаёт подкласс, поэтому подходит, если нужен тип реализации, но не может наследовать `final`-класс или переопределять `final`-метод. В обоих случаях вызов должен пройти через прокси: если целевой объект сам вызывает свой метод через `this`, [обёртка этого не увидит](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html).

### Замер и переключатель в одном процессе

[JMX](../../04%20JVM%20и%20производительность/Мониторинг%20и%20диагностика%20JVM/JMX%20—%20MBean%20и%20MBeanServer.md) (*Java Management Extensions*) — API Java для наблюдения и управления. *MBean* — объект, который выставляет через этот API свой интерфейс управления; это не обязательно Spring-бин. Регистрируем контроллер в платформенном `MBeanServer` под именем `profiling:name=controller`. Пара `isEnabled()` / `setEnabled()` образует в JMX доступный для чтения и записи атрибут `Enabled`. Обычное соглашение Standard MBean — класс `ProfilingController` и интерфейс `ProfilingControllerMBean`; в примере явно связываем их через [`StandardMBean`](https://docs.oracle.com/en/java/javase/25/docs/api/java.management/javax/management/StandardMBean.html).

Переключатель — `volatile`, потому что JMX меняет его из другого потока: [запись видна при последующем чтении](https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html#jls-17.4.5). Проверяем флаг один раз в начале вызова, поэтому смена значения не отменяет уже начавшийся замер. Это не [Spring profiles и `@Profile`](../Spring%20Boot/Профили%20и%20@Profile.md): бин уже создан, прокси остаётся тем же, меняется только его поведение на следующих вызовах.

Второй блок — продолжение `Demo.java`. Обработчик рассчитан на обычный singleton из примера с одним напрямую объявленным публичным интерфейсом. Его задача — показать, где проходит граница между before и after, а не заменить Spring AOP.

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
                        // у самой обёртки сравнение по ссылке; эти методы не замеряем
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

Интересно, что для замера нужен не календарь: по контракту [`System.nanoTime()`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/System.html#nanoTime()) имеет смысл разность двух показаний, а не значение часов само по себе. `finally` печатает время и при исключении, а из [`InvocationTargetException`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/InvocationTargetException.html#getCause()) достаём исходную причину, чтобы вызывающий код не получил служебную обёртку рефлексии. Замер включает делегирование через рефлексию; это наблюдение за вызовом, а не микробенчмарк.

### Собираем пример и щёлкаем флаг

Последний блок закрывает `Demo.java`. Оба BPP объявлены через `static @Bean` с типом обработчика в сигнатуре: контекст распознаёт их заранее и не поднимает конфигурацию раньше времени ради создания обработчиков.

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

Для запуска нужны Maven и JDK 25. Рядом с `Demo.java` сохраним `pom.xml`:

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

В конструкторе будет `0`, в `init()` — число от 2 до 6. Жмём Enter: приложение печатает цитаты без замера. Затем в другом терминале запускаем `jconsole` и в **Local Process** выбираем JVM по напечатанному PID. В **MBeans → profiling → controller → Attributes** меняем `Enabled` на `true`. Снова жмём Enter в терминале приложения: после цитат появится `terminatorQuoter.sayQuote: … нс`. Возвращаем `false` — следующего замера нет. Не пересоздавали ни бин, ни прокси, ни контекст.

Здесь легко ослышаться: речь о JMX-консоли, а не о Consul. [В докладе (45:57)](https://www.youtube.com/watch?v=BmBr5diz8WA&t=2757s) переключение показывают через Java VisualVM с плагином MBeans, а мы используем [JConsole из JDK](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jconsole.html). Для локального подключения от того же пользователя удалённый порт и конфигурация удалённого JMX не нужны.

## Что имеем по итогу

До `init()` настраиваем сам объект; после `init()` можем подставить обёртку для будущих вызовов. Если нужно запустить логику уже *через* прокси после подготовки контекста, одного `@PostConstruct` недостаточно — этот случай отдельно разбирается в [статье про ContextRefreshedEvent и @PostInitialize](Трёхфазный%20конструктор%20—%20ContextRefreshedEvent%20и%20@PostInitialize.md).

> [!QUESTION]- Проверь себя: вопросы с собеседований, которые закрывает статья
> - Как устроена цепочка `BeanPostProcessor` и что значит вернуть `null`?
> - Где в жизненном цикле работают before и after и почему прокси обычно возвращают из after?
> - Как зарегистрировать обработчик и записать число в `private`-поле до `init()`?
> - Кто обрабатывает `@Autowired` и `@PostConstruct` и почему важен порядок BPP?
> - Зачем сохранять имя и класс бина до оборачивания? Что нужно передать JDK-прокси?
> - Как замерять вызов, не потерять исходное исключение и переключать замеры через JMX на лету?

## Ссылки

* [Евгений Борисов, «Spring-потрошитель»](https://www.youtube.com/watch?v=BmBr5diz8WA) — исходный доклад.
* [JUG Ru, текстовая версия доклада](https://habr.com/ru/companies/jugru/articles/893638/) — исторический пример с XML, кворером и JMX.
* [Spring Framework: BeanPostProcessor](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/config/BeanPostProcessor.html) — контракт, порядок и регистрация обработчиков.
* [Spring Framework: совместное использование методов инициализации](https://docs.spring.io/spring-framework/reference/core/beans/factory-nature.html#beans-factory-lifecycle-combined-effects) — порядок `@PostConstruct`, `afterPropertiesSet()` и собственного `init`-метода.
* [Исходник Spring 6.2.11: цепочки before и after](https://github.com/spring-projects/spring-framework/blob/v6.2.11/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java#L423-L451) — как следующий обработчик получает результат предыдущего.
* [Spring Framework: ReflectionUtils.setField()](https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/org/springframework/util/ReflectionUtils.html#setField(java.lang.reflect.Field,java.lang.Object,java.lang.Object)) — запись значения в поле через рефлексию.
* [Spring Framework: прокси в AOP](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html) — различия JDK Dynamic Proxy и CGLIB и ограничение вызовов через `this`.
* [JDK: ThreadLocalRandom.nextInt()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ThreadLocalRandom.html#nextInt(int,int)) — границы диапазона.
* [JDK: Class.getInterfaces()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Class.html#getInterfaces()) и [Proxy.newProxyInstance()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/Proxy.html#newProxyInstance(java.lang.ClassLoader,java.lang.Class%5B%5D,java.lang.reflect.InvocationHandler)) — откуда берутся интерфейсы и как создаётся JDK-прокси.
* [JDK: System.nanoTime()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/System.html#nanoTime()) и [InvocationTargetException.getCause()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/InvocationTargetException.html#getCause()) — замер интервала и извлечение исходного исключения.
* [JLS §17.4.5](https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html#jls-17.4.5) — видимость записи в `volatile` между потоками.
* [JDK: StandardMBean](https://docs.oracle.com/en/java/javase/25/docs/api/java.management/javax/management/StandardMBean.html) и [JConsole](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jconsole.html) — интерфейс управления и локальное подключение.
