# Устройство Spring WebMVC и DispatcherServlet

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Схема обработки запроса: DispatcherServlet → HandlerMapping → контроллер → ModelAndView → ViewResolver → View
* DispatcherServlet как фронт-контроллер: поэтапное делегирование модулям
* Два контейнера веб-приложения: веб-слой (контроллеры) и сервисный слой, вложенность контекстов
* Настройка ViewResolver: prefix, suffix, класс представления, кэширование шаблонов
* Root WebApplicationContext (сервисы, репозитории, источники данных) и Servlet WebApplicationContext (контроллеры, ViewResolver, HandlerMapping): делегирование, если бин не найден
* Как работает Spring Web MVC
* Путь запроса в Spring Web MVC: поток Tomcat → DispatcherServlet → HandlerMapping → HandlerAdapter → HttpMessageConverter
* Обработка исключений и почему весь запрос занимает один поток
* Как запрос проходит через Spring MVC?
* Сколько потоков у Tomcat по умолчанию (200)
