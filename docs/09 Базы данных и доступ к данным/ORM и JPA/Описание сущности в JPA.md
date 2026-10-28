# Описание сущности в JPA

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* JPA как стандарт (JSR-220): маппинг, EntityManager, JPQL, Criteria API; реализации Hibernate ORM, EclipseLink, DataNucleus
* Требования к классу сущности: @Entity, конструктор без аргументов, класс верхнего уровня, не final, Serializable при передаче по значению
* Требования к полям: инкапсуляция, доступ через поля или через свойства
* Требования к первичному ключу: @Id или @EmbeddedId, допустимые типы, @GeneratedValue
* Как реализовать equals и hashCode у сущности: id = null до persist, Hibernate-прокси и getClass(), бизнес-ключ; почему не @Data из Lombok
