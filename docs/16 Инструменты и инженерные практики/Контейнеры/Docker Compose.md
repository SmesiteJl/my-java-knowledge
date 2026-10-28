# Docker Compose

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Основы Docker, термины и концепции
* Dockerfile, создание образа, запуск контейнера и развёртывание приложений; команды Docker: docker build -t, docker run -d -p --name, docker-compose up -d, down, build
* Dockerfile Java-приложения на каждый сервис, готовый jar в образе: FROM eclipse-temurin:21-jre-alpine, WORKDIR, COPY --from=build (многоэтапная сборка), EXPOSE, ENTRYPOINT с java -jar
* Docker Compose: docker-compose.yml для многоконтейнерных приложений; сервисы: build, image, ports, environment, именованные volumes (пример с postgres:15)
* Volumes и networks: хранение данных вне контейнера (volume против bind mount), связь контейнеров по имени, типы сетей (bridge, host, none)
* Как дождаться готовности базы при старте: healthcheck и depends_on с condition: service_healthy
* docker-compose на сервис: приложение, PostgreSQL, Liquibase-мигратор, общая внешняя сеть, переменные окружения; run-local.sh — сборка bootJar и запуск compose-файлов по очереди
