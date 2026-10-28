# Persistence Context, EntityManager и состояния сущности

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* EntityManager и основные методы: persist, find, merge, remove, detach, createQuery
* Persistence Context как кэш первого уровня и пул объектов: уникальность объекта по PK
* Состояния сущности: new (transient), managed, detached, removed
* Прокси-объекты в ORM и метод getReference()
* Переходы между состояниями сущности: persist, find и getReference, detach, clear, close, merge, remove, flush
* Какие бывают состояния сущности Hibernate (entity states)
* Что такое persistence context
* Состояния сущности Transient, Managed, Detached, Removed и переходы persist, merge, detach/evict/clear/close, remove, flush, find
* Жизненный цикл объекта в Session: что Hibernate отслеживает до и после close()
* Инкремент счётчика через сущность в @Transactional-методе: чем опасен такой код
* Состояния сущности и persistence context
* Что такое dirty checking
* Состояния Transient, Managed, Detached, Removed и переходы между ними
* Пример по строкам: почему изменение после session.close() не попало в базу
* Dirty checking и flush: когда Hibernate пишет UPDATE без вызова save
* Инкремент через сущность как lost update (слайд 12)
* Что такое persistence context и dirty checking?
* Какие состояния сущности в Hibernate?
* Когда Hibernate пишет UPDATE, если save не вызывали?
* Изменили объект после закрытия сессии. Попадёт ли это в базу? Что делает merge?
* Где lost update, если инкремент делать через сущность, и как его закрыть?
