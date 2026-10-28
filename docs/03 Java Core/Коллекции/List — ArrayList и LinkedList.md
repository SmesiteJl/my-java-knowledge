# List: ArrayList и LinkedList

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* ArrayList: Object[] внутри, size и capacity, расширение массива; свой список на массиве с System.arraycopy
* Удаление из ArrayList: сдвиг через System.arraycopy, рост ёмкости в 1,5 раза, почему массив не уменьшается (trimToSize)
* LinkedList: двусвязный список Node(prev, element, next), реализация List и Deque
* Сложность get, add, remove, contains у ArrayList, LinkedList и CopyOnWriteArrayList; почему LinkedList на практике почти всегда медленнее ArrayList даже на вставках: локальность кэша, накладные расходы на узел
* ArrayList против Vector; почему Stack и Vector устарели и чем их заменить (ArrayDeque, интерфейс Deque)
