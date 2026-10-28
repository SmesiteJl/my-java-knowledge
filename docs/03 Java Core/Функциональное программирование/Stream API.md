# Stream API

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Stream как декларативная обработка коллекций функциями высших порядков; отличие от потоков ввода-вывода; сравнение процедурного и функционального стиля обработки коллекции
* Стадии работы со стримом: создание (collection.stream(), Arrays.stream, Stream.of, String.chars(), Files.lines), конвейерные и терминальные операции
* Функциональные интерфейсы Stream API: Predicate, Consumer, Function, Supplier, UnaryOperator, BinaryOperator
* Конвейерные операции: filter, map, flatMap (в том числе по вложенным коллекциям), skip, limit, peek, sorted, distinct, mapToInt (mapToInt().sum())
* Терминальные операции: collect, min и max, average, sum, count, reduce, anyMatch, allMatch, noneMatch, forEach; невозможность переиспользовать завершённый стрим
* reduce с Optional и без начального значения; sorted с компаратором
* Коллекторы: toList, toSet, toMap (в том числе с merge-функцией), toCollection, groupingBy (в том числе с counting — число студентов по каждому баллу), reducing
* Ленивость стримов: без терминальной операции ничего не выполняется (peek ничего не выведет), элементы проходят конвейер по одному
* Короткое замыкание: findFirst, anyMatch, limit; что вернёт allMatch на пустом стриме
* Бесконечные стримы generate + limit; задача на категоризацию компаний по сотрудникам
* Параллельные стримы: общий ForkJoinPool, когда они не быстрее, проблемы с порядком, состоянием и побочными эффектами; forEach против forEachOrdered
* Когда не стоит использовать Stream API: производительность на малых данных, отладка, checked-исключения в лямбдах
* Примеры: первые 4 нечётных числа × 17, подсчёт уникальных символов строки
* groupingBy, reduce на примерах Employee и Money; Optional.map
* Лайвкодинг: средняя зарплата по отделам через groupingBy и averagingDouble, затем отдел с максимальной средней
