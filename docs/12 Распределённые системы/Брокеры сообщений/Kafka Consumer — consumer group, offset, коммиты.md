# Kafka Consumer: consumer group, offset, коммиты

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Что такое consumer group и как партиции распределяются между консьюмерами: одну партицию читает один потребитель группы; что если консьюмеров больше, чем партиций
* Offset и его коммит, где Kafka хранит offset группы (топик __consumer_offsets); типы коммитов: автокоммит (at most once) и ручной (at least once) — когда сообщения теряются, а когда дублируются
* commitSync и commitAsync: в чём разница и когда что использовать
* spring-kafka: @KafkaListener и режимы подтверждения (AckMode)
* Ребалансировка и её стратегии: eager против cooperative (incremental), static membership — зачем они нужны
* Что происходит при падении консьюмера: heartbeat, session.timeout.ms, max.poll.interval.ms, ребаланс и повторная обработка незакоммиченных сообщений
* Новый протокол ребаланса KIP-848 (GA в 4.0): назначение партиций на стороне брокера, group.protocol=consumer, чем он лучше eager и cooperative
* Как перечитать сообщения: seek, сброс offset группы, auto.offset.reset earliest и latest, чтение конкретной партиции
* Consumer lag: что это, как мониторить и что делать, если консьюмеры не успевают (больше партиций и консьюмеров, батчи, backpressure)
* Обработка ошибок в консьюмере: «ядовитое» сообщение, retry-топики и DLT (DefaultErrorHandler, @RetryableTopic в spring-kafka)
