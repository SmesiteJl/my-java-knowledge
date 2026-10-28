# Модульное тестирование с JUnit

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Зачем нужно модульное тестирование
* Модульное тестирование в Java: JUnit 5 (Jupiter), JUnit 4, TestNG; JUnit 3 (наследование от TestCase, методы test*, setUp и tearDown) и JUnit 4: аннотации @Test, @Before, @BeforeClass, @After, @AfterClass
* Основные конструкции: @Test, Assertions.assertEquals; assert-методы (assertTrue, assertFalse, assertEquals, assertArrayEquals, assertNotEquals, assertSame, assertNotSame, fail); именование тестов (Test, test, should)
* Окружение теста (fixture) и жизненный цикл тестового класса: экземпляр на каждый тест, setUp/tearDown; аннотации жизненного цикла в JUnit 4 и JUnit 5: @BeforeAll/@BeforeClass, @BeforeEach/@Before, @AfterEach/@After, @AfterAll/@AfterClass, @Rule
* Параметры @Test: expected и timeout; проверка исключения через try и fail
* @Ignore и Assume
* Почему нежелательно несколько assert в одном тесте и нельзя полагаться на порядок тестов
* Ручной запуск тестов: JUnitCore.runClasses и Result.getFailures; запуск методов test* через рефлексию с новым экземпляром класса на каждый тест
* JUnit 5 против JUnit 4: Platform, Jupiter и Vintage, модель расширений @ExtendWith вместо @RunWith и @Rule; assertThrows, assertAll, @Nested, @DisplayName
* Параметризованные тесты в JUnit 5: @ParameterizedTest с @ValueSource, @CsvSource, @MethodSource
