# JVM в контейнере: лимиты памяти и CPU, выбор GC

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Как JVM видит лимиты контейнера: UseContainerSupport, MaxRAMPercentage против -Xmx; почему -Xmx, равный лимиту пода, — ошибка
* Почему RSS важнее размера кучи: что кроме heap занимает память контейнера (metaspace, стеки потоков, code cache, direct buffers) и почему под получает OOMKilled без OutOfMemoryError
* Что вернёт availableProcessors() при CPU limit, как от него зависят число GC-потоков и ForkJoinPool, откуда берётся CPU throttling (CFS quota)
* Какой GC выберет JVM в поде с 1 CPU или меньше 1792 МБ до JDK 27 и что изменил JEP 523
* Requests и limits для Java-сервиса: как выбрать и почему memory request часто ставят равным limit
