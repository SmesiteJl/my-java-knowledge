# Iterable и Iterator

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Разница Iterator и Iterable
* Методы итератора hasNext() и next(); обход коллекции итератором
* Iterable: Collection наследует Iterable, Map — нет (обход через entrySet)
* Iterator: методы hasNext() и next(); метод iterator() у коллекции
* Связь Iterator и цикла for-each (с Java 5)
* Обход коллекции итератором: пример
* Свой Iterator/Iterable (бесконечный генератор чётных чисел)
* Безопасное удаление из коллекции через removeIf
* Fail-fast и fail-safe итераторы: modCount и expectedModCount, почему ConcurrentModificationException возникает и в одном потоке, какие коллекции дают weakly consistent итераторы
* Iterator против ListIterator; Enumeration против Iterator
