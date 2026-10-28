# Загрузка классов и ClassLoader

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Иерархия загрузчиков классов (Bootstrap, Platform, Application) и модель делегирования родителю: зачем она нужна
* Как JVM идентифицирует класс (полное имя плюс загрузчик); почему один и тот же класс из двух загрузчиков даёт ClassCastException
* Этапы жизни класса: loading, linking (verification, preparation, resolution), initialization; когда именно выполняется статическая инициализация
* Что будет при исключении в статическом блоке инициализации: ExceptionInInitializerError, а при следующем обращении NoClassDefFoundError
* ClassNotFoundException против NoClassDefFoundError; NoSuchMethodError при конфликте версий зависимостей
