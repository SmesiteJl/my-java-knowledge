# Spring Data JPA

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Что такое Spring Data JPA и зачем он нужен: избавление от шаблонного DAO-кода
* Репозитории JpaRepository и готовые CRUD-методы
* Как в Spring Data JPA можно сделать запрос: метод по имени (derived queries), @Query с JPQL и нативным SQL, @Modifying, Specification, Example, проекции, пагинация
* Пагинация и сортировка: Pageable, Sort, Page
* Specification, проекции, @EnableJpaRepositories
* Как save() решает, вызвать persist или merge (isNew по id и @Version); почему при заданном вручную id появляется лишний SELECT и как помогает Persistable
