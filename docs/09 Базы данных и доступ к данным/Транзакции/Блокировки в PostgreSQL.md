# Блокировки в PostgreSQL

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Режимы табличных блокировок PostgreSQL (ACCESS SHARE … ACCESS EXCLUSIVE): что с чем конфликтует, какие блокировки берут ALTER TABLE и CREATE INDEX
* Строковые блокировки: FOR UPDATE, FOR NO KEY UPDATE, FOR SHARE, FOR KEY SHARE; NOWAIT
* Как PostgreSQL обнаруживает deadlock (deadlock_timeout, откат одной из транзакций) и как его расследовать через pg_locks и pg_stat_activity
* Advisory locks: распределённая блокировка средствами PostgreSQL
