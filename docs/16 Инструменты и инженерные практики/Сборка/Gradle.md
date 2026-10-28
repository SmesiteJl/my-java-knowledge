# Gradle

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Gradle как декларативно-императивный сборщик; gradle и gradlew (wrapper)
* settings.gradle: имя проекта и многомодульность
* build.gradle: plugins, repositories (mavenCentral, mavenLocal), dependencies (implementation, testImplementation)
* Нет фиксированного жизненного цикла: задачи от плагинов (плагин java), свои задачи с doFirst/doLast
* Структура Gradle-проекта: settings.gradle, подпроекты с build.gradle.kts, buildSrc; описание сборки на Groovy или Kotlin DSL
* Стандартные задачи плагина java: assemble, build, check, clean, compileJava, jar, javadoc, test и др.; порядок выполнения doFirst и doLast
