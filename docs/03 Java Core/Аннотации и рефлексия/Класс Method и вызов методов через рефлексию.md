# Класс Method и вызов методов через рефлексию

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Классы рефлексии: Method, Field, Constructor, Annotation, Type, Package
* Интроспекция: getMethods (getName, getReturnType, getParameterTypes) и getFields
* Рефлексия и инкапсуляция: getMethods и getFields против getDeclaredMethods и getDeclaredFields
* Сигнатура метода в рефлексии: имя и массив Class параметров (getMethod("indexOf", String.class, int.class)); Class у примитивов
* Varargs: объявление Object... и вызов с произвольным числом аргументов
* Вызов метода через invoke и создание объектов по введённым именам классов; getConstructor
* Управление поведением без перекомпиляции (примеры EvilGuy и FileConverter); рефлексия как основа фреймворков
* Чтение аннотаций через рефлексию (getAnnotations и instanceof Author); связь с @Override и аннотациями JUnit
