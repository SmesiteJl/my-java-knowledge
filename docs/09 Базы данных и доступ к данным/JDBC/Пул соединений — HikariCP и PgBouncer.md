# Пул соединений: HikariCP и PgBouncer

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Почему соединение с PostgreSQL дорогое (процесс на соединение) и зачем нужен пул
* Размер пула HikariCP: maximumPoolSize, minimumIdle, connectionTimeout; почему больший пул не значит быстрее
* Пул исчерпан («Connection is not available»): длинная @Transactional держит соединение, внешний вызов внутри транзакции, утечки и leakDetectionThreshold
* PgBouncer: зачем внешний пул, режимы session, transaction, statement и ограничения transaction-режима
