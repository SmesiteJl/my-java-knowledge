# Класс Object и его методы

`Object` — верхушка дерева наследования в Java. Поскольку Java — объектно-ориентированный язык, внутри core-пакета и не только соблюдаются три столпа: полиморфизм, инкапсуляция и, конечно же, наследование. Вот как раз `Object` существует для соблюдения столпов.

Точнее, двух из них. Как говорит [документация `java.lang.Object`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Object.html):

> Класс `Object` — корень иерархии классов. У каждого класса `Object` — суперкласс. Все объекты, включая массивы, реализуют методы этого класса.

Класс без `extends` неявно наследуется от `Object` — это наследование. А значит, любой объект можно передать туда, где ждут `Object`, — это полиморфизм: на нём держится и `equals(Object obj)`, и любой код, которому всё равно, какой объект пришёл. К инкапсуляции `Object` отношения не имеет.

Как у настоящего класса, у него есть свои методы, а раз так — эти методы есть и у любого объекта в Java. Список методов:

1. `toString()`
2. `equals(Object obj)`
3. `hashCode()`
4. `getClass()`
5. `clone()`
6. `wait()`
7. `wait(long timeout)`
8. `wait(long timeout, int nanos)`
9. `notify()`
10. `notifyAll()`
11. `finalize()`

По сути это пять групп: описание объекта (`toString()`, `getClass()`), сравнение и хеш (`equals()`, `hashCode()`), копирование (`clone()`), работа с потоками (три `wait()`, `notify()`, `notifyAll()`) и жизненный цикл (`finalize()`).

До нас дожили все 11, но `finalize()` доживает последние релизы. Метод был сначала помечен как `deprecated` в Java 9, затем — `deprecated for removal` в Java 18 ([JEP 421](https://openjdk.org/jeps/421)). При этом в актуальной LTS-версии (Java 25) он **всё ещё есть** в [исходном коде класса `Object`](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/java/lang/Object.java#L608) — пустой и помеченный на удаление:

```java
@Deprecated(since="9", forRemoval=true)
protected void finalize() throws Throwable { }
```

Удалить его могут в любом следующем релизе, а JVM, запущенная с флагом `--finalization=disabled`, уже сейчас не вызывает ни одного финализатора.

Теперь подробно про каждый.

## `toString()`

```java
public String toString() {
    return getClass().getName() + "@" + Integer.toHexString(hashCode());
}
```

Имя класса, `@` и хеш объекта в шестнадцатеричном виде. Почему там именно хеш и что будет после переопределения `hashCode()` — разобрано в [статье про `equals()` и `hashCode()`](Контракт%20equals%20и%20hashCode.md#хеш-в-tostring).

Переопределяем, когда хотим видеть в логах содержимое объекта, а не хеш:

```java
@Override
public String toString() {
    return "Programmer{salary=" + salary + ", position=" + position + "}";
}
```

`record` генерирует похожий `toString()` сам — по всем компонентам.

## `equals()`

```java
public boolean equals(Object obj) {
    return (this == obj);
}
```

Есть [статья про `equals()`](Контракт%20equals%20и%20hashCode.md#сравнение-по-ссылке-equals-по-умолчанию), где можно прочитать подробнее. Но если кратко, то это обёртка над оператором `==`.

## `hashCode()`

```java
@IntrinsicCandidate
public native int hashCode();
```

А вот здесь тела нет вовсе. `native` значит, что метод реализован не на Java, а на C++ внутри самой JVM, поэтому в IDEA в него и не провалиться. Обычным Java-кодом его не написать: хеш хранится в заголовке объекта, а до заголовка из Java не дотянуться.

Таких методов в `Object` шесть: `getClass()`, `hashCode()`, `clone()`, `notify()`, `notifyAll()` и приватный `wait0()`, через который работают все три `wait()`. Все они делают то, чего на Java не сделать: узнают настоящий класс объекта, лезут в его заголовок, копируют память, работают с монитором.

Аннотация `@IntrinsicCandidate` — подсказка, что HotSpot может подменить метод заранее написанным машинным кодом, *интринсиком*. Её ставят не только на `native`-методы: в `Object` она висит даже на пустом конструкторе.

Что именно `hashCode()` делает внутри, откуда берётся число и почему это не адрес в памяти — разобрано в [статье про `equals()` и `hashCode()`](Контракт%20equals%20и%20hashCode.md#native-тела-на-java-нет).

> [!QUESTION]- Проверь себя: вопросы с собеседований, которые закрывает статья
> - `Object` как корень иерархии и группы его методов
> - `toString()` по умолчанию и его переопределение
> - `equals()` и `hashCode()` по умолчанию

## Ссылки

* [Документация `java.lang.Object` (Java 25)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Object.html) — все методы класса и их контракты
* [Исходник `Object.java` в JDK 25](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/java/lang/Object.java) — какие методы `native`, а какие написаны на Java
* [JEP 421: Deprecate Finalization for Removal](https://openjdk.org/jeps/421) — почему финализацию убирают из Java
