# RabbitMQ: модель AMQP и сравнение с Kafka

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Типы exchange в RabbitMQ: direct, fanout, topic (шаблоны * и #), headers; binding и routing key
* Подтверждения в RabbitMQ: auto и manual ack, nack/reject с requeue, prefetch (basicQos) и равномерное распределение между консьюмерами
* Dead Letter Exchange: когда сообщение уходит в DLX (reject без requeue, истёк TTL, переполнение очереди) и как сделать отложенный retry через TTL + DLX
* Как не потерять сообщение в RabbitMQ: durable-очереди, persistent-сообщения, publisher confirms, quorum queues
* Чем RabbitMQ отличается от Kafka: push-очередь против pull-журнала, удаление после ack против retention, маршрутизация, порядок, масштабирование; когда что выбрать
* Share groups в Kafka 4.2 — очередь поверх топика с подтверждением каждой записи: что это меняет в сравнении с RabbitMQ
