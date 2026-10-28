# Mock-объекты и Mockito

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Назначение библиотек mock-тестирования и mock-объектов: изоляция тестируемого модуля от зависимостей (БД, сеть, файлы)
* Тестовые дублёры: stub, mock, fake
* Основные возможности Mockito — подмена зависимостей: Mockito.mock + when/thenReturn для зависимости, переданной через конструктор; пример с базой данных — подмена DAO моком и проверка логики сервиса
* Mockito: mock(InputStream.class), when(...).thenReturn(...), значения по умолчанию для неописанных методов; пример — тест суммы первых n байтов без реального файла
* assertEquals для double с дельтой
* @Mock против @InjectMocks и MockitoExtension в JUnit 5; чем @Mock отличается от @MockitoBean в Spring-тесте
* Проверка вызовов: verify и ArgumentCaptor для проверки аргумента вызова, отсутствие вызовов (never(), verifyNoInteractions, InOrder); как замокать void-метод (doThrow, doNothing, doAnswer)
* Mock против Spy в Mockito: когда нужен spy и почему для него используют doReturn().when(), а не when().thenReturn()
* Argument matchers: правило «все аргументы матчеры или ни одного», any() против eq(); strict stubs и UnnecessaryStubbingException
* Ограничения Mockito: final-классы, static-методы (mockStatic), конструкторы; почему частый mockStatic — признак проблем в дизайне
* Тестирование REST-эндпоинтов: пример RestAssured и @QuarkusTest
* Когда не нужно мокать: избыточная верификация и тесты, привязанные к реализации
