# Срезы тестов: @WebMvcTest, @DataJpaTest, @MockitoBean

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* @WebMvcTest + @ContextConfiguration с @TestConfiguration: тест контроллера с замоканным DAO, проверка контракта и JSON-ответа через MockMvc, jsonPath и status()
* @DataJpaTest и TestEntityManager
* @MockBean внутри @SpringBootTest и модульный тест сервиса с Mockito без контекста; почему @MockBean и @SpyBean удалены в Spring Boot 4 и чем их заменяют @MockitoBean и @MockitoSpyBean
* Что изменилось с MockMvc в Boot 4: @SpringBootTest без @AutoConfigureMockMvc, новый RestTestClient
