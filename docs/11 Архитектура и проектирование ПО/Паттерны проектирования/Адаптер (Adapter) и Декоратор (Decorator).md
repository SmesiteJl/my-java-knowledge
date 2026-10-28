# Адаптер (Adapter) и Декоратор (Decorator)

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Суть: динамическое добавление поведения через обёртку
* Пример SimpleCoffee + MilkDecorator
* Где применять; декораторы в java.io (PrintWriter, BufferedReader поверх потоков сокета)
* Тип (структурный) и структура: Component, ConcreteComponent, Decorator, ConcreteDecorator; гибкая альтернатива наследованию
* Суть: совместная работа объектов с несовместимыми интерфейсами
* Пример MediaPlayer / VLCPlayer / MediaAdapter
* Адаптеры в Java: JDBC-драйвер, OutputStreamWriter; адаптеры к сторонним библиотекам
* Тип (структурный) и структура: Client, целевой интерфейс, Adapter, Adaptee
* Декоратор: новое поведение существующего объекта с сохранением старых методов; схема класса B, оборачивающего A
* Адаптер: преобразование одного интерфейса в другой (пример Lamp и SmartLampForDevice)
* Разница декоратора и адаптера: интерфейс расширяется или заменяется
* Адаптер и декоратор в java.io: BufferedReader(InputStreamReader(InputStream)), BufferedInputStream(FileInputStream)
* Адаптер Costable → Priceable для подключения legacy-репозитория к калькулятору
