# Динамические прокси: java.lang.reflect.Proxy и ByteBuddy

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Proxy.newProxyInstance: ClassLoader, список интерфейсов, InvocationHandler
* Ограничение JDK-прокси: проксируемый класс должен реализовывать интерфейсы
* ByteBuddy: прокси-наследник через subclass(), method(), intercept()
* JDK-прокси против CGLIB, ByteBuddy и Javassist: интерфейсы против наследования классов
* ByteBuddy: MethodDelegation.to, make(), load(...).getLoaded() и создание экземпляра
* Proxy.newProxyInstance: три аргумента — ClassLoader, список интерфейсов, InvocationHandler
* Метод invoke(proxy, method, args) и делегирование исходному объекту через method.invoke
* Куда загружается сгенерированный класс прокси (heap в Java 8, PermGen в Java 7)
* ByteBuddy: subclass(type).method(any()).intercept(InvocationHandlerAdapter.of(...)) как альтернатива CGLIB
* Подсчёт вызовов @Deprecated-методов в InvocationHandler
