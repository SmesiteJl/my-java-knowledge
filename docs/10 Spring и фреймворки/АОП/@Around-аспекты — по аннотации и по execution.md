# @Around-аспекты: по аннотации и по execution

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* @Around("@annotation(...)") с ProceedingJoinPoint: замер времени и своя «транзакция» (open/commit/rollback)
* CGLIB-прокси для класса без интерфейсов: что вернёт getClass() бина с аспектом
* Pointcut execution(* com.example.demo.services..*.say*(..)), ProceedingJoinPoint.proceed() и getTarget()
* spring.aop.proxy-target-class=false: JDK-прокси вместо CGLIB, который Boot 2 использует по умолчанию
* Pointcut "@within(Benchmark) || @annotation(Benchmark)": аннотация на классе или на методе
* Чтение аннотации метода через MethodSignature
* Self-invocation: вызов собственного метода через самовнедрённый прокси, чтобы аспект сработал
* spring.main.allow-circular-references=true: Boot 2.6+ по умолчанию запрещает циклические ссылки
