# Comparable, Comparator и PriorityQueue

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Comparable.compareTo: естественный порядок, заданный в самом классе
* Comparator.compare: внешний порядок, передача в конструктор TreeSet и в Stream API
* Пример сортировки объектов в TreeSet через Comparable и через Comparator
* Зачем описывать сравнение своих объектов: Collections.sort и упорядоченные коллекции
* Comparable<T>.compareTo: смысл отрицательного, нулевого и положительного результата (пример Student)
* Comparator<T>.compare: отдельный класс и анонимный класс, передача в Collections.sort
* Comparable против Comparator: одна естественная сортировка или сколько угодно внешних
* PriorityQueue: извлечение по приоритету; порядок через Comparable или Comparator в конструкторе
* Контракт compareTo и Comparator: согласованность с equals, транзитивность; почему TreeSet «теряет» элементы при compare == 0
