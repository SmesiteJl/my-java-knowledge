# CompletableFuture вместо блокирующих вызовов

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Проблема последовательных блокирующих вызовов и решение через цепочку supplyAsync → handleAsync → thenAccept
* thenApply, thenCompose и thenCombine; allOf и anyOf — как комбинировать несколько CompletableFuture
* Обработка ошибок в CompletableFuture: exceptionally, handle, whenComplete; что происходит с цепочкой после исключения
* Таймауты и отмена в CompletableFuture: orTimeout, completeOnTimeout, cancel; join против get
* Лайвкодинг: параллельно опросить N сервисов через CompletableFuture и собрать результаты с общим таймаутом
