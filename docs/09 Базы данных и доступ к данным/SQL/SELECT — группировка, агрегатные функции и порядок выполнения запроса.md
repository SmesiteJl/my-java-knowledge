# SELECT: группировка, агрегатные функции и порядок выполнения запроса

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Логический порядок выполнения SELECT: FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT; почему алиас из SELECT нельзя использовать в WHERE
* GROUP BY: какие столбцы можно выводить в SELECT при группировке и как GROUP BY обрабатывает NULL
* Агрегатные функции: COUNT(*) против COUNT(column) против COUNT(DISTINCT column), как агрегаты обрабатывают NULL
* Чем WHERE отличается от HAVING и когда без HAVING не обойтись
* GROUP BY против DISTINCT: в чём разница и что выбрать для устранения дублей
* UNION против UNION ALL, INTERSECT и EXCEPT: что возвращают и почему UNION дороже
