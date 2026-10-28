# Прокси в Spring: JDK Dynamic Proxy и CGLIB

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Два способа незаметно подменить бин: реализовать те же интерфейсы (dynamic proxy) или унаследоваться от класса (CGLIB)
* Ограничения CGLIB: final-классы и final-методы
* Как Spring AOP выбирает тип прокси: есть интерфейсы — dynamic proxy, нет — CGLIB
* Почему бин нужно получать по интерфейсу, а не по классу реализации (getClass() вернёт $Proxy7)
* Выбор типа прокси: есть интерфейсы — Proxy.newProxyInstance, нет — CGLIB Enhancer
* Пример: логирование вызовов класса, помеченного @Deprecated
* @Before("@annotation(Deprecated) && ebayMethods()") — комбинирование pointcut-ов
* spring.aop.proxy-target-class=true: CGLIB-прокси вместо JDK
