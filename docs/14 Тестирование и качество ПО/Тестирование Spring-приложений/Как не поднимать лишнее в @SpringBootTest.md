# Как не поднимать лишнее в @SpringBootTest

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* @SpringBootTest(classes = TestEnvConfig.class) с @ComponentScan(lazyInit = true) или spring.main.lazy-initialization=true: поднимаются только нужные тесту бины
* @EnableJpaRepositories(bootstrapMode = BootstrapMode.LAZY)
* @MockBean для ненужных зависимостей; @TestConfiguration с @Primary-заменами (ручной мок репозитория и Mockito.mock)
* Condition, проверяющий запуск из JUnit (по stack trace) с переопределением через свойство и кэшированием в static-поле
* Кэширование контекста Spring TestContext: что ломает кэш (@MockitoBean, разные профили и свойства, @DirtiesContext) и как ускорить набор интеграционных тестов
