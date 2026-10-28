# @Transactional в Spring: прокси, откат, propagation

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Что было до: ручное управление транзакцией
* Что такое @Transactional и как он работает: AOP-прокси вокруг бина, транзакция открывается на входе в метод и фиксируется или откатывается на выходе
* Почему @Transactional не работает при вызове из того же класса: что будет, если метод вызывает другой @Transactional-метод того же класса
* На каких исключениях транзакция откатывается: unchecked и checked, откатится ли она при IOException, rollbackFor и noRollbackFor; почему после checked Exception записи остались (тест «expected 0 but was 2»)
* Propagation: REQUIRED, REQUIRES_NEW, SUPPORTS, NOT_SUPPORTED, MANDATORY, NEVER, NESTED; чем REQUIRED отличается от REQUIRES_NEW и NESTED
* UnexpectedRollbackException: внутренний REQUIRED-метод бросил исключение, внешний его поймал — почему транзакция всё равно откатилась (rollback-only)
* Атрибут isolation и прочие атрибуты @Transactional
* @Transactional(readOnly = true): что даёт Hibernate (FlushMode.MANUAL, без dirty checking), JDBC (setReadOnly) и маршрутизации на реплику; что будет при записи внутри такой транзакции
* Можно ли поставить @Transactional на метод, который ходит по REST в другой сервис
* Программное управление транзакциями: PlatformTransactionManager и TransactionTemplate — когда они лучше декларативного @Transactional
