# The equals and hashCode contract

## Reference equality: the default `equals()`

* `==` is a plain reference comparison: different reference values mean different objects, even if all their fields match.
* By default, `equals()` is also a plain reference comparison. Here it is in [`Object`](Класс%20Object%20и%20его%20методы.md):
  ```java
  public boolean equals(Object obj) {
      return (this == obj);
  }
  ```
  In other words, the `==` operator is built right into it.

So the default `equals()` is just a wrapper around `==`. The comparison always returns `false` unless we pass in the very same object. If we want `equals()` to compare objects the way we need it to, we override it.

### Primitives and the `Integer` cache gotcha

With primitives (`int`, `long`, `double`, `boolean`…), there are no references: `==` compares the values themselves, which is exactly what we want. Objects, on the other hand, come with a few gotchas that interviewers love:

```java
Integer a = 127, b = 127;
System.out.println(a == b);      // true
Integer c = 128, d = 128;
System.out.println(c == d);      // false with HotSpot's default cache
```

Why? [Autoboxing](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/Синтаксис%20и%20типы/Классы-обёртки%20и%20автоупаковка/) (Russian) calls [`Integer.valueOf()`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Integer.html#valueOf(int)). It always caches values from `-128` through `127`, but it can cache values outside that range too. So both `127`s get the same object, while the two `128`s get different objects with HotSpot's default cache. The second result isn't guaranteed by Java.

Strings are similar: `"java"` literals live in the [*string pool*](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/Строки/Класс%20String%20—%20создание,%20сравнение%20и%20пул%20строк/) (Russian) and refer to one object, while `new String("java")` always creates a new one.

**The takeaway is simple:** use `equals()` to compare objects, and save `==` for primitives and for asking, “Is this the very same object?”

## Overriding `equals()`

### What the docs require

According to the [`java.lang.Object` docs](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Object.html#equals(java.lang.Object)), `equals()` needs to have these properties:

> - **Reflexivity:** for any non-null reference `x`, `x.equals(x)` should return `true`.
> - **Symmetry:** for any non-null references `x` and `y`, `x.equals(y)` should return `true` if and only if `y.equals(x)` returns `true`.
> - **Transitivity:** for any non-null references `x`, `y`, and `z`, if `x.equals(y)` returns `true` and `y.equals(z)` returns `true`, then `x.equals(z)` should return `true`.
> - **Consistency:** for any non-null references `x` and `y`, repeated calls to `x.equals(y)` should always return `true` or always return `false`, provided none of the information used in `equals` comparisons on those objects has changed.
> - For any non-null reference `x`, `x.equals(null)` should return `false`.

Notice that the docs themselves point us to `hashCode()` and `HashMap`:

> **See Also:** `hashCode()`, `java.util.HashMap`

And the docs spell out the contract, too:

> **API Note:** It is generally necessary to override the `hashCode` method whenever this method is overridden, so as to maintain the general contract for the `hashCode` method, which states that equal objects must have equal hash codes.
>
> **Implementation Requirements:** The `equals` method for class `Object` implements the most discriminating possible equivalence relation on objects; that is, for any non-null reference values `x` and `y`, this method returns `true` if and only if `x` and `y` refer to the same object (`x == y` has the value `true`). In other words, under the reference equality equivalence relation, each equivalence class only has a single element.

### The implementation

Here's an example override:

```java
@Override
public boolean equals(Object obj) {
    // check reflexivity: an object is always equal to itself
    if (this == obj) return true;
    // check the fifth rule: comparing with null gives false.
    // this itself is never null: we can't call a method on null without getting a NullPointerException first.
    // then check that both objects are of the same class: if their classes differ, return false
    if (obj == null || getClass() != obj.getClass()) return false;
    // now we know both objects are of the same class, so we can safely cast
    Programmer that = (Programmer) obj;
    // then compare fields. We don't have to compare every field, by the way:
    // we get to decide which fields are enough to call the objects equal.
    // Objects.equals() is null-safe: two nulls are equal, but null and a non-null value aren't
    return salary == that.salary && Objects.equals(position, that.position);
}
```

The `Objects.equals()` call on the last line is really simple under the hood. Here it is in [`java.util.Objects`](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/java/util/Objects.java#L61):

```java
public static boolean equals(Object a, Object b) {
    return (a == b) || (a != null && a.equals(b));
}
```

The cheap `==` check comes first and also catches the case where both references are `null`. Only then do we call `equals()`, and only on an object we know isn't `null`. That's why it's easier to use `Objects.equals()` for reference fields than to write `position.equals(that.position)`, which throws a `NullPointerException` if `position` is `null`.

### Inheritance: calling `super.equals()`

With [inheritance](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/ООП/Наследование/) (Russian), we do the same thing, but we call the superclass's `equals()` first:

```java
@Override
public boolean equals(Object obj) {
    // call the superclass method through super. If the objects already differ there, return false.
    // If they match there, they can still differ on the fields the subclass adds.
    if (!super.equals(obj)) return false;
    // we can safely cast here, thanks to the getClass() != obj.getClass() check in the superclass.
    // The neat part: getClass() runs on the object we called the method on, so the superclass checks
    // whether obj is a MiddleProgrammer, not a Programmer as we might expect. See the footnote.
    MiddleProgrammer that = (MiddleProgrammer) obj;
    // now compare whichever subclass fields we care about
    return grade == that.grade;
}
```

Why does `getClass()` in the superclass see the subclass? That's in the footnote[^getclass].

### `instanceof` instead of `getClass()`

If our inheritance model lets us compare superclass and subclass instances directly, we can use `instanceof`:

```java
@Override
public boolean equals(Object obj) {
    if (this == obj) return true;
    if (!(obj instanceof Programmer)) return false; // also rules out null
    Programmer that = (Programmer) obj;
    return Objects.equals(name, that.name);
}
```

And the subclass needs its own `instanceof` check:

```java
@Override
public boolean equals(Object obj) {
    if (this == obj) return true;
    if (!(obj instanceof MiddleProgrammer)) return false; // we need this check in the subclass
    if (!super.equals(obj)) return false;
    MiddleProgrammer that = (MiddleProgrammer) obj;
    return level == that.level;
}
```

### The catch: we just broke symmetry

Now let's test this pair against the rules in the docs. Take a `Programmer` and a `MiddleProgrammer` with the same name:

```java
Programmer p = new Programmer("Вася");
MiddleProgrammer m = new MiddleProgrammer("Вася", 3);

p.equals(m); // true: m instanceof Programmer, and the names match
m.equals(p); // false: p isn't an instance of MiddleProgrammer
```

`p` is equal to `m`, but `m` isn't equal to `p`: **we broke symmetry**. This is the “give me an example of broken symmetry” question that comes up in interviews. If we try to fix it in the subclass (“when comparing with a plain `Programmer`, just check the name”), we break transitivity instead: two `MiddleProgrammer` objects with different levels can both be equal to the same `Programmer` but not to each other.

So we can't compare superclass and subclass instances and also add new fields to the subclass's `equals()`. We have to pick one of three approaches:

| Approach | How it works | Trade-off |
|---|---|---|
| `getClass()` | Objects of different classes are never equal | Symmetry holds, but a subclass instance is never equal to a superclass instance, even if they represent the same thing |
| `instanceof` + `final` `equals()` in the superclass | Subclasses can't override equality or add fields to the comparison | Works only when subclasses differ in behavior, not in data |
| Composition instead of inheritance | `MiddleProgrammer` holds a `Programmer` instead of extending it | More wrapper code, but each class has its own `equals()` without breaking the contract |

Joshua Bloch recommends the third approach in [*Effective Java*](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/). Item 10 is all about the `equals` contract.

### Where Hibernate comes in

One place `getClass()` can trip us up is with *JPA entities*. With [lazy loading](https://smesitejl.github.io/my-java-knowledge/ru/09%20Базы%20данных%20и%20доступ%20к%20данным/ORM%20и%20JPA/Ленивая%20загрузка,%20проблема%20N+1%20и%20скрытый%20SQL/) (Russian), Hibernate slips in a *proxy* instead of the entity itself: a generated subclass like `Programmer$HibernateProxy$…`. The proxy and the actual entity can represent the same database row, but `getClass()` returns different classes for them. An `equals()` that checks `getClass()` will call them different. So with entities, the usual approach is:

* use `instanceof` (or `Hibernate.getClass()`) rather than `getClass()`;
* compare by `id`: an entity without an `id` (one we haven't saved yet) is equal only to itself;
* have `hashCode()` return a constant for the class (for example, `getClass().hashCode()`), since the `id` doesn't appear until the entity is saved and the hash shouldn't change while the object is in a `HashSet`;
* keep lazy collections out of `equals()` and `hashCode()`, which is why using [Lombok](https://smesitejl.github.io/my-java-knowledge/ru/16%20Инструменты%20и%20инженерные%20практики/Инструменты%20разработчика/Lombok/) (Russian) `@Data` or `@EqualsAndHashCode` on entities is risky.

[Vlad Mihalcea](https://vladmihalcea.com/the-best-way-to-implement-equals-hashcode-and-tostring-with-jpa-and-hibernate/) goes through this approach in detail, with tests.

> [!SUMMARY] In short
> `equals()` compares objects by their contents so we can tell whether two different objects in our program represent the same thing in the real world.

## Overriding `hashCode()`

### What the docs require

Here's what the [docs](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Object.html#hashCode()) say:

> The general contract of `hashCode` is:
>
> - **Consistency.** Whenever it is invoked on the same object more than once during an execution of a Java application, the `hashCode` method must consistently return the same integer, provided no information used in `equals` comparisons on the object is modified. This integer need not remain consistent from one execution of an application to another execution of the same application.
> - **Equal objects give equal hash codes.** If two objects are equal according to the `equals` method, then calling the `hashCode` method on each of the two objects must produce the same integer result.
> - **Unequal objects can have the same hash code.** It is *not* required that if two objects are unequal according to the `equals` method, then calling the `hashCode` method on each of the two objects must produce distinct integer results. However, the programmer should be aware that producing distinct integer results for unequal objects may improve the performance of hash tables.

In short, equal objects are guaranteed to have **the same** `hashCode`, while unequal ones **don't have to have different ones**. `hashCode()` returns an `int`, and there are only `4,294,967,296` possible `int` values. That makes *collisions* unavoidable: different objects can have the same `hashCode`.

```java
@IntrinsicCandidate
public native int hashCode();
```

That's the original native `hashCode()` in `Object`. In HotSpot, it gives us the object's hash using Marsaglia's *xor-shift* algorithm, built into the JVM[^xorshift].

### `native`: no Java method body

Here's what I wondered:

> *Why can't I jump into the implementation of `hashCode()`?*

There's no Java code to jump into. `native` means the method has no Java body: it's implemented in C++ inside the JVM itself (HotSpot), so IntelliJ IDEA has nothing to open. And Cmd+click (Ctrl+click on Windows and Linux) on the method name where it's declared runs *Go to Declaration or Usages*. When we're already at the declaration, it looks for usages instead. That's where “No usages found” comes from.

`@IntrinsicCandidate` adds another layer. It means HotSpot can replace the method with an *intrinsic*: machine code written for that operation[^intrinsic]. The JIT compiler does just that with `hashCode()`: it reads the hash straight from the object header and goes to the native function only if the hash isn't there yet. So even the C++ implementation doesn't tell the whole story.

Here's where to find the real implementation in the OpenJDK sources:

* [`jvm.cpp`, the `JVM_IHashCode()` function](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/hotspot/share/prims/jvm.cpp#L622): the entry point from `Object.hashCode()`;
* [`synchronizer.cpp`, `ObjectSynchronizer::FastHashCode()`](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/hotspot/share/runtime/synchronizer.cpp#L989) and `get_next_hash()` next to it: this is where the hash is generated and written into the object header. We'll see exactly how in the section on identity hashCode below.

### Implementing it with `Objects.hash()`

We override it (along with `equals()`, of course):

```java
@Override
public int hashCode() {
    return Objects.hash(salary, position);
}
```

This one's much simpler: we call `Objects.hash()` with the fields we compare in `equals()`. **The very same fields:** if `hashCode()` uses a field that `equals()` ignores, equal objects can end up with different hashes, and we've broken the contract.

With inheritance:

```java
@Override
public int hashCode() {
    return Objects.hash(super.hashCode(), grade);
}
```

`Objects.hash()` looks pretty simple under the hood:

```java
public static int hash(Object... values) {
    return Arrays.hashCode(values);
}
```

It calls `Arrays.hashCode()`, which is where the actual work happens:

```java
public static int hashCode(Object[] a) {
    if (a == null)
        return 0;

    int result = 1;

    for (Object element : a)
        result = 31 * result + (element == null ? 0 : element.hashCode());

    return result;
}
```

One small detail to remember: `Objects.hash()` takes *varargs*, so a call like ours creates an array and boxes any primitives. That's extra work on a hot path, so there we'd write `hashCode()` ourselves with the same `31 * result + …` formula. And for a [`record`](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/Новые%20версии%20Java/Records/) (Russian), the compiler generates both `equals()` and `hashCode()` from all the components.

### Why 31?

No magic. It just happens to be a good fit:

* **It's odd.** Multiplying by an even number always leaves the lowest bit at zero. In effect, there's a left shift in there. At each step zeros build up in the low bits, and when `int` overflows, the high bits just fall off. The early fields' contributions gradually get washed out. That doesn't happen with an odd multiplier.
* **It's prime.** The idea is that a prime multiplier mixes the bits better and is less likely to “resonate” with patterns in the input. That's more tradition than hard math: being odd is what really matters here. [Chapter 6.3 of *hello-algo*](https://www.hello-algo.com/ru/chapter_hashing/hash_algorithm/) (Russian) explains why primes are useful in hash functions. In fact, it writes the multiplicative hash exactly as `hash = 31 * hash + c`.
* **Multiplying by it is cheap:** `31 * i == (i << 5) - i`, a shift and a subtraction instead of a multiplication. A modern JVM makes that substitution on its own.

The same formula is in [`String.hashCode()`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#hashCode()): s[0]·31ⁿ⁻¹ + s[1]·31ⁿ⁻² + … + s[n−1], where n is the length of the string. Javadoc writes it with `^`, but there it means exponentiation, not Java's XOR. That gives us a classic collision: `"Aa"` and `"BB"` both hash to `2112`.

### The hash in `toString()`

By the way!

When we write

```java
System.out.println(programmer);
```

without overriding `toString()`, we get something like:

```text
com.username.src.equalshashcode.Programmer@e580929
```

That `e580929` is just the object's hash in hexadecimal. We get it because the call goes to `Object`'s `toString()`, which looks like this:

```java
public String toString() {
    return getClass().getName() + "@" + Integer.toHexString(hashCode());
}
```

Notice that `toString()` calls `hashCode()` itself, not some separate “system” hash. If we override `hashCode()`, the part after `@` is whatever hash our override returns.

### Identity hashCode

If we don't override `hashCode()`, what follows `@` is the *identity hashCode*: a hash of the object's identity, not its contents. That's the native `hashCode()` from `Object`.

A common myth is that it's the object's address in memory. **No.** The [garbage collector](https://smesitejl.github.io/my-java-knowledge/ru/04%20JVM%20и%20производительность/Память%20JVM%20и%20сборка%20мусора/Сборка%20мусора%20—%20принципы%20и%20поколения/) (Russian) moves objects around: from Eden to Survivor, into Old, and during compaction. The address changes, but the contract says the `hashCode` must stay the same. Here's what HotSpot does:

1. Until someone asks for its `hashCode`, the object doesn't have one.
2. On the first call, the JVM generates a random number using Marsaglia's xor-shift. Each thread has its own generator state so the threads don't get in each other's way.
3. The number is trimmed to fit the bits set aside in the object header (the *mark word*) and written there.
4. Later calls just read the value from the header. The hash stays the same for the object's entire life, no matter where the GC moves it.

The JVM does have a “return the address” mode (`-XX:hashCode=4`), but that's an experimental flag. The default is `5`, xor-shift. You can see all the modes in the [HotSpot source](https://github.com/openjdk/jdk/blob/master/src/hotspot/share/runtime/synchronizer.cpp), in `get_next_hash()`.

We can get the identity hashCode even if `hashCode()` has been overridden, with `System.identityHashCode(obj)`:

```java
Programmer a = new Programmer(1000, "Java");
Programmer b = new Programmer(1000, "Java");

System.out.println(a.hashCode() == b.hashCode());                         // true: our hashCode() uses the fields
System.out.println(System.identityHashCode(a) == System.identityHashCode(b)); // almost certainly false: these are two different objects
```

`IdentityHashMap`, for example, is built around identity hashes. It compares keys with `==` rather than `equals()`.

## How this works in `HashMap`

Now for the main point: why do we need the contract at all? When we insert a key into a [`HashMap`](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/Коллекции/HashMap%20—%20устройство,%20коллизии%20и%20ресайз/) (Russian) or an element into a `HashSet` (which is backed by a `HashMap`), here's what happens:

1. `HashMap` takes `key.hashCode()` and mixes it with `h ^ (h >>> 16)`: the high bits get mixed into the low bits.
2. It uses the hash to get the *bucket* index: `(n - 1) & hash`, where `n` is the table size (always a power of two).
3. Within that bucket, `HashMap` goes through the entries and checks each one: does the hash match? If so, is it the same object (`==`) or an equal one (`equals()`)?

In other words, it compares two numbers first and pays for the more expensive `equals()` only if the hashes match.

### We only overrode `equals()`

```java
Programmer a = new Programmer(1000, "Java");
Programmer b = new Programmer(1000, "Java");

a.equals(b);                    // true: we overrode equals()

Set<Programmer> set = new HashSet<>();
set.add(a);
set.add(b);
set.size();                     // 2, but we expected 1
set.contains(new Programmer(1000, "Java"));   // false
```

We still have `Object`'s `hashCode()`. `a` and `b` have different identity hashes and almost certainly land in different buckets, so we never even get to `equals()`. We end up with duplicates in a `Set` and a `get()` that can't find what we're looking for.

Here are all four possibilities in one place:

| What we overrode | What happens in `HashSet` |
|---|---|
| Neither method | Each object is unique: equality is by reference. That's fine for services and beans, but not for objects we want to compare by value |
| Only `equals()` | Equal objects usually land in different buckets: duplicates creep in, and `contains()` and `get()` can't find an equivalent object |
| Only `hashCode()` | Objects with equal values land in the same bucket, but reference-based `equals()` says they're different, so the duplicates stay |
| Both | It works as intended: one element per value |

### `hashCode()` always returns a constant

```java
@Override
public int hashCode() {
    return 42;
}
```

This is perfectly legal under the contract: equal objects have equal hashes. But every entry lands in the same bucket, and `HashMap` turns into a list: every `get()` and `put()` has to go through the entries with `equals()`, `O(n)` instead of `O(1)`. Since Java 8, a bucket with more than 8 entries can turn into a red-black tree (once the table has capacity 64 or more), which can bring that down to `O(log n)`. But the tree orders keys using `compareTo()`, and if they aren't `Comparable`, the ordering is practically arbitrary and doesn't help much. So a constant `hashCode()` works, but it's slow.

The contract is the bare minimum. A good `hashCode()` also spreads different objects across different numbers as evenly as possible. That's exactly what the third point in the docs is about: distinct hash codes for unequal objects can improve [hash table](https://smesitejl.github.io/my-java-knowledge/ru/02%20Алгоритмы%20и%20структуры%20данных/Множества%20и%20словари/Хеш-таблицы%20—%20HashSet%20и%20HashMap/) (Russian) performance.

### We changed a key field after `put()`

```java
Map<Programmer, String> map = new HashMap<>();
Programmer key = new Programmer(1000, "Java");
map.put(key, "команда платежей");

key.setSalary(2000);            // hashCode() uses this field

map.get(key);                   // null
map.containsKey(key);           // false
map.size();                     // 1: the entry hasn't gone anywhere
```

The entry is still in the bucket we picked using the old hash. Now we're looking it up with the new hash, so we look in the wrong bucket. The entry is “lost”: we can't get it by its key, but it's still taking up memory.

**Here's the rule:** `HashMap` keys and `HashSet` elements should be [immutable](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/ООП/Неизменяемые%20объекты/) (Russian). Think `String`, `Integer`, `record`, or our own immutable classes. Or at least make sure the fields `hashCode()` uses don't change while the object is in the collection.

### Collisions and `TreeMap`

If hashing isn't working out because we have too many collisions or can't write a good `hashCode()`, there's [`TreeMap` and `TreeSet`](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/Коллекции/Map%20—%20LinkedHashMap,%20TreeMap,%20EnumMap%20и%20IdentityHashMap/) (Russian). They don't use `hashCode()` or `equals()` at all to compare keys. Instead, they use `compareTo()` (or a supplied [`Comparator`](https://smesitejl.github.io/my-java-knowledge/ru/03%20Java%20Core/Коллекции/Comparable,%20Comparator%20и%20PriorityQueue/) (Russian)), and we get guaranteed `O(log n)` lookups, insertions, and removals.

There's a gotcha here, too: `compareTo()` needs to be consistent with `equals()` for the usual set or map semantics to hold. The classic example is `BigDecimal`:

```java
BigDecimal x = new BigDecimal("1.0");
BigDecimal y = new BigDecimal("1.00");

x.equals(y);        // false: their scales differ
x.compareTo(y);     // 0

new HashSet<>(List.of(x, y)).size();   // 2
new TreeSet<>(List.of(x, y)).size();   // 1
```

Same numbers, different set sizes depending on the implementation.

## When we can skip the overrides

We need to override `equals()` and `hashCode()` when objects have logical equality: two separate objects can represent the same thing, whether that's an amount of money, a set of coordinates, or a programmer with certain details. We call those *value objects*. We don't need to override the methods when each object has its own identity and reference equality is already what we want:

* **services, controllers, Spring beans, and singletons**: there's one instance, so there's nothing to compare;
* **`enum`**: there's only one instance per constant, and its `equals()` is already `final` and compares references;
* **identity-based objects** like a `Thread` or a database connection: two different connections aren't equal, even if they're configured the same way;
* **`record`**: the compiler already generated `equals()` and `hashCode()` from all the components;
* **a subclass** that doesn't add fields to the comparison can use its superclass's `equals()`.

## Where that leaves us

`equals()` and `hashCode()` do related jobs, but they do them differently. `hashCode()` returns an `int` from a hash function. `equals()` compares references (and/or fields if we override it, which we need to do in most cases).

**Objects that are equal according to `equals()` must have the same `hashCode`, but matching hashes don't mean the objects are equal.** That's why hash-based collections start with `hashCode()`: the hash check is faster. A match is no guarantee that the objects are actually equal. It just tells us to go to the next step and call `equals()`, which gives us the final answer.

Why not start with `equals()`? Because most of the time the objects are different: comparisons end in `false` more often than in `true`. So we can use the faster hash check for those 80% of cases and afford to go slower on the other 20%. That's worth keeping in mind when we write code: make the “not equal” path fast, because proving equality costs more than ruling it out.

> [!QUESTION]- Check yourself: interview questions this article covers
> - How does `equals()` work by default, and how is it different from `==`? What does `==` do with primitives?
> - What properties does `equals()` need to satisfy: reflexivity, symmetry, transitivity, consistency, and `x.equals(null) == false`?
> - How do we implement `equals()` with the `this`, `null`, and `getClass()` checks and field comparisons?
> - When do we use `getClass()` or `instanceof` in `equals()`? How can inheritance break symmetry, and where do Hibernate proxies come in?
> - How do we implement `hashCode()`? Which fields matter, where do `Objects.equals()` and `Objects.hash()` fit in, and why multiply by 31?
> - What does the default `hashCode()` return, why isn't it a memory address, and what does `System.identityHashCode()` do?
> - Why do we need to override both methods? What happens in a `HashSet` or `HashMap` if we don't?
> - How do `HashMap.put()` and `HashSet.add()` use `hashCode()` and `equals()`?
> - What happens if `hashCode()` always returns a constant?
> - What happens if we change a key field that `hashCode()` uses after `put()`?
> - What is a `hashCode` collision, and how does `TreeMap` avoid relying on hashes?
> - When can we skip overriding `equals()` and `hashCode()`?

%%///Footnotes Go Here///%%

[^getclass]:
    **Why `getClass()` in the superclass's `equals()` returns the subclass.**

    Here's what I wondered:

    > *We're calling a superclass method from `MiddleProgrammer`, and the `getClass()` call is in the superclass's code. So isn't `getClass()` called on the superclass?*

    That mixes up two different things: **whose code runs** and **what object it runs on**.

    `super.equals(obj)` changes only the first part: we're running the `equals()` code written in `Programmer`. The object stays the same. There's no separate “superclass object” inside `MiddleProgrammer`. There's one object, with fields from both the superclass and the subclass.

    So when `getClass()` runs in the superclass's code, it's really `this.getClass()`, and `this` is still the same `MiddleProgrammer` object.

    **An analogy.** Say your name is Vasya, and you're following instructions your dad wrote. One line says, “Say your name.” You read it and say “Vasya,” not your dad's name. He wrote the instructions, but you're carrying them out. Same thing here:

    * the instructions are the `equals()` code from `Programmer`;
    * the one following them is the `MiddleProgrammer` object;
    * the line that says “say your name” is `getClass()`.

    **What `getClass()` does.** It's declared `final` in `Object`, so nobody overrides it. It doesn't know which class the call was written in. It just looks at the object it was called on and returns its actual class, the one named after `new`. We can check that:

    ```java
    class Programmer {
        void whoAmI() {
            System.out.println(getClass().getSimpleName());
        }
    }
    class MiddleProgrammer extends Programmer {}

    new Programmer().whoAmI();          // Programmer
    new MiddleProgrammer().whoAmI();    // MiddleProgrammer
    ```

    There's only one `whoAmI()` implementation, and it's in the superclass. But it prints something different depending on the object we call it on.

[^xorshift]:
    **Marsaglia's xor-shift algorithm.** A pseudorandom number generator George Marsaglia proposed in 2003. It keeps a few numbers as state and mixes them at each step with shifts (`<<`, `>>`) and exclusive OR (`^`). That's fast: just a few CPU instructions, and it produces well-distributed numbers. HotSpot uses it by default for identity hashCode, with a separate generator state for each thread.

    * [Xorshift: explanation and code examples (Wikipedia)](https://en.wikipedia.org/wiki/Xorshift)
    * [George Marsaglia, “Xorshift RNGs,” *Journal of Statistical Software*, 2003](https://doi.org/10.18637/jss.v008.i14) — the original paper
    * [HotSpot source: `get_next_hash()` in `synchronizer.cpp`](https://github.com/openjdk/jdk/blob/master/src/hotspot/share/runtime/synchronizer.cpp) — all `hashCode` generation modes; mode `5` is xor-shift

[^intrinsic]:
    **What an intrinsic is.** The Javadoc for [`@IntrinsicCandidate`](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/jdk/internal/vm/annotation/IntrinsicCandidate.java) puts it this way:

    > The `@IntrinsicCandidate` annotation is specific to the HotSpot Virtual Machine. It indicates that an annotated method may be (but is not guaranteed to be) intrinsified by the HotSpot VM. A method is intrinsified if the HotSpot VM replaces the annotated method with hand-written assembly and/or hand-written compiler IR — a compiler intrinsic — to improve performance.

    The annotation is internal to the JDK's own libraries. We don't use it in our code. In the C2 JIT compiler, the intrinsic for `hashCode()` is `LibraryCallKit::inline_native_hashcode()` in [`library_call.cpp`](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/hotspot/share/opto/library_call.cpp#L4689): it takes the hash from the object header or calls the regular `hashCode()` if the header doesn't have it yet.

## Links

* [Java Kabala, “Java from Scratch: equals and hashCode”](https://www.youtube.com/watch?v=N2z_1EGSN4U) (Russian) — a half-hour lesson on the contract, overrides, and inheritance, with simple examples
* [`java.lang.Object` documentation (Java 25)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Object.html) — the original `equals` and `hashCode` contracts
* [`Integer.valueOf(int)` documentation (Java 25)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Integer.html#valueOf(int)) — which values are guaranteed to be cached
* [*hello-algo*, chapter 6.3, “Hashing Algorithms”](https://www.hello-algo.com/ru/chapter_hashing/hash_algorithm/) (Russian) — how hash functions work and why they use prime numbers
* [HotSpot source: `synchronizer.cpp`](https://github.com/openjdk/jdk/blob/master/src/hotspot/share/runtime/synchronizer.cpp) — the `get_next_hash()` function and all the identity hashCode generation modes
* [HotSpot source: `JVM_IHashCode()` in `jvm.cpp`](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/hotspot/share/prims/jvm.cpp#L622) — where the native `Object.hashCode()` actually goes
* [`java.util.Objects` source (JDK 25)](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/java/util/Objects.java) — the full implementations of `Objects.equals()` and `Objects.hash()`
* [Vlad Mihalcea: how to implement `equals()` and `hashCode()` for JPA and Hibernate entities](https://vladmihalcea.com/the-best-way-to-implement-equals-hashcode-and-tostring-with-jpa-and-hibernate/)
* [Joshua Bloch, *Effective Java*, 3rd edition](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/) — Items 10 and 11 cover `equals` and `hashCode` (the Russian edition is titled «Java. Эффективное программирование»)
