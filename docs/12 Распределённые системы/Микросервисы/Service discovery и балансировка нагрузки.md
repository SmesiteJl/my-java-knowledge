# Service discovery и балансировка нагрузки

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Балансировка нагрузки между копиями приложения, аналогия с репликацией БД
* Стратегии выбора узла: круговая схема (round robin), наименьшее время ответа, показатели загрузки, данные запроса
* Балансировщик как фасад и обратный прокси
* Зачем нужен service discovery: проблема захардкоженных URL при переносе между средами
* Части механизма: реестр, регистрация, проверка здоровья, выбор экземпляра; как сервис регистрируется в Discovery Server и как другой сервис получает его URL по имени
* Client-side и server-side discovery
* Алгоритмы балансировки: round robin, random, weighted, least connections, consistent hashing
* Крайние случаи: экземпляр упал между проверками, упал реестр, экземпляр не прогрет, сервис из Docker зарегистрировался под внутренним адресом
* Готовые решения: Eureka, Consul, DNS Kubernetes; регистрация сервисов в Consul (spring-cloud-starter-consul-discovery)
* Связка Discovery с клиентским балансировщиком (Ribbon + RestTemplate) и декларативным клиентом OpenFeign; межсервисные вызовы через OpenFeign (UserClient, CartClientService)
* Вызов сервиса по имени из реестра (http://MATH/exercise/random) через @LoadBalanced RestTemplate; два RestTemplate в контексте: @Primary обычный и @LoadBalanced, @LoadBalanced как квалификатор параметра конструктора
* ДЗ 1: свой реестр сервисов — потокобезопасность, Math.floorMod в round robin
* Как сервис находит другой сервис в облаке? Что такое service discovery?
* Чем client-side discovery отличается от server-side?
* Экземпляр упал между проверками здоровья. Что будет и что делает клиент?
