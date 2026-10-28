# Области памяти JVM (Runtime Data Areas)

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Из каких областей состоит память JVM: heap, стеки потоков с фреймами, Metaspace, code cache, PC-регистр, native-стек — что где хранится
* PermGen и Metaspace: что изменилось в Java 8 и почему
* Сколько памяти занимает объект: заголовок (mark word, klass pointer), выравнивание, сжатые указатели (Compressed OOPs); оценка памяти на элемент ArrayList и LinkedList
* Параметры памяти: -Xms, -Xmx, -Xss, -XX:MaxMetaspaceSize; почему часто ставят Xms = Xmx; MaxRAMPercentage в контейнере
