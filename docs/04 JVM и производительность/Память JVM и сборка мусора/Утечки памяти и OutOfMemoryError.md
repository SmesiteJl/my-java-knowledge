# Утечки памяти и OutOfMemoryError

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Как в Java получить утечку памяти при наличии GC: статические коллекции, кэши без вытеснения, незакрытые ресурсы, ThreadLocal в пулах, слушатели, внутренние классы
* Виды OutOfMemoryError: Java heap space, Metaspace, GC overhead limit exceeded, unable to create new native thread, Direct buffer memory; чем отличается StackOverflowError
* Что происходит при OutOfMemoryError, можно ли его поймать и продолжить работу; -XX:+HeapDumpOnOutOfMemoryError
* Как найти утечку памяти: пилообразный график, heap dump, Eclipse MAT — dominator tree и retained size
