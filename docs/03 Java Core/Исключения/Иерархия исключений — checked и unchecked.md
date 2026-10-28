# Иерархия исключений: checked и unchecked

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Исключение: определение и зачем нужна обработка исключений вместо кодов ошибок
* Иерархия: Throwable → Error и Exception → RuntimeException
* Проверяемые (checked) и непроверяемые (unchecked) исключения и их связь с иерархией
* Разница между Error и RuntimeException
* Примеры известных исключений: Error — OutOfMemoryError, StackOverflowError; checked — IOException, FileNotFoundException, ClassNotFoundException, SQLException, NoSuchMethodException; unchecked — ArithmeticException, IndexOutOfBoundsException, IllegalArgumentException, NullPointerException
* Создание собственного класса исключения: когда делать его checked, а когда unchecked; почему Spring и современные фреймворки используют unchecked
