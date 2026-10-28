# Модель Producer-Consumer: wait, notify, notifyAll

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Модель Producer-Consumer: постоянный обмен результатами между потоками (аналогия «кухня и официанты»); постановка задачи — ограниченный буфер
* Проблема активного ожидания пустыми циклами while (!product.isReady())
* Методы Object wait, notify, notifyAll: снятие блокировки на время ожидания и пробуждение потоков; почему они вызываются только внутри synchronized (IllegalMonitorStateException) и почему условие wait проверяют в цикле (spurious wakeup)
* Чем отличаются sleep, wait и yield и какой из них отпускает монитор; notify против notifyAll
* Реализация produce и consume (Producer и Consumer) через synchronized(product), wait в цикле while и notify
* Запуск потоков производителя и потребителя, join
* Как неправильная реализация приводит к взаимной блокировке
* Лайвкодинг: ограниченный буфер на ReentrantLock и Condition
