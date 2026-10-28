# JDBC: архитектура и основные интерфейсы java.sql

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* JDBC как стандарт доступа к СУБД; драйвер как адаптер под протокол конкретной СУБД
* DriverManager и загрузка драйвера через Class.forName; почему имя драйвера держат в properties
* Connection: getConnection(url, user, password), закрытие через try-with-resources
* Statement, PreparedStatement, CallableStatement — различия; почему PreparedStatement быстрее (прекомпиляция, пакетные вставки)
* executeQuery, executeUpdate, execute — когда что и что возвращают
* ResultSet: next(), getXxx по имени столбца, закрытие
* Плюсы JDBC (любая реляционная БД, полный контроль) и минусы (один SQLException, ручной маппинг, нет понимания связей FK-PK)
* Обработка SQLException: getSQLState, getErrorCode, перевод в свои исключения (SQLState 23505 → UniqueSqlException)
* Что такое JDBC
* Что такое JDBC: java.sql, драйвер, DataSource и пул соединений HikariCP
* PreparedStatement и защита от SQL-инъекции
* Почему JDBC блокирующий и что вместо него в реактивном стеке (R2DBC)
