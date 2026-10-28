# Maven

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Что такое сборка и процесс сборки; что получается на выходе (jar, war)
* Что входит в проект: исходники, зависимости, файлы конфигурации окружения, статические ресурсы, предкомпилируемые стили, код на других языках, файлы среды разработки и тестов
* Артефакт/релиз и проект разработки: почему их структура различается
* Минусы ручной сборки и задачи сборщика: управление зависимостями, компиляция, тесты, раскладка файлов, развёртывание, ведение проекта
* Императивный и декларативный подходы к описанию сборки
* Обзор сборщиков: Ant, Maven, Gradle, Make, Composer, NPM, Webpack
* Maven как декларативный сборщик; возможности: компиляция, зависимости, тесты, плагины, Wagon, SCM, задачи Ant
* Создание проекта из архетипа: mvn archetype:generate с groupId, artifactId, archetypeArtifactId
* Стандартная структура: pom.xml, src/main/java, resources, webapp, src/test, target; простой и веб-проект
* pom.xml: groupId, artifactId, version, packaging, properties, dependencies, plugins; scope зависимостей (compile, provided, runtime, test, system, import) — где какой и какие из них транзитивны
* Жизненный цикл: validate, compile, test, package, integration-test, verify, install, deploy и clean; запуск фазы выполняет все предыдущие
* Репозитории: Maven Central, локальный ~/.m2, удалённые
* SNAPSHOT и релизные версии; чем mvn install отличается от mvn deploy
* Родительский POM, dependencyManagement и BOM в многомодульном проекте
* Как Maven разрешает конфликт версий транзитивных зависимостей (nearest wins); dependency:tree, exclusions и фиксация версии в dependencyManagement
* Профили Maven: как активируются и зачем нужны
* Maven или Gradle: чем отличаются подходы и что бы вы выбрали для нового проекта
