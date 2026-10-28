# Библиотеки логирования в Java

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* JUL (java.util.logging)
* SLF4J как фасад над реализациями логирования; получение логгера: Logger.getLogger (JUL) и LoggerFactory.getLogger (SLF4J)
* Logback и его конфигурация (logback.xml, logback-spring.xml): ConsoleAppender, encoder и pattern (%d, %thread, %-5level, %logger, %msg), traceId и spanId в шаблоне, уровень root
* Части логгера: config, appender, encoder, layout, filter (onMatch и onMismatch)
* Уровни логирования по пакетам в Spring Boot: logging.level.*
* Как организовать логирование в сервисе: уровни по окружениям, JSON-логи, MDC с traceId и его передача в другие потоки
* Как правильно логировать исключения и что нельзя писать в лог (персональные данные, секреты); маскирование
