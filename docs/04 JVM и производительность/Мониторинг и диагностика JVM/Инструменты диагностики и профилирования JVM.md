# Инструменты диагностики и профилирования JVM

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Как снять thread dump и heap dump (jstack, jcmd, jmap) и что в них искать
* Мониторинг GC: GC-логи (-Xlog:gc), jstat, метрики пауз и аллокаций
* Профилирование: JFR и JDK Mission Control, async-profiler, VisualVM — как найти причину высокой загрузки CPU или медленного метода
* Микробенчмарки: почему замер System.nanoTime в цикле врёт и как помогает JMH (прогрев, dead code elimination)
