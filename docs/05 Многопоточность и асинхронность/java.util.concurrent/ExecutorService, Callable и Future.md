# ExecutorService, Callable и Future

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Fixed и cached пулы: порядок выполнения задач
* Callable и Future: Runnable против Callable, invokeAll, получение результатов через Future — get с таймаутом, cancel(mayInterruptIfRunning), isDone, FutureTask
* Как устроен ThreadPoolExecutor: corePoolSize, maximumPoolSize, keepAliveTime, очередь; в каком порядке создаются потоки и ставятся задачи
* Чем опасны фабрики Executors: неограниченная очередь у newFixedThreadPool, неограниченное число потоков у newCachedThreadPool
* Политики отказа RejectedExecutionHandler: Abort, CallerRuns, Discard, DiscardOldest
* Как выбрать размер пула для CPU-bound и IO-bound задач
* ScheduledExecutorService: scheduleAtFixedRate против scheduleWithFixedDelay
