# Kubernetes: развёртывание сервисов

> [!NOTE] Тема в работе
> Статьи по этой теме пока нет. Вот вопросы, на которые она ответит.

* Из чего состоит Kubernetes: control plane (API server, etcd, scheduler, controller manager) и рабочие ноды (kubelet, kube-proxy, container runtime)
* Pod, ReplicaSet и Deployment: что это, как связаны и что указывают в манифесте Deployment
* Service и его типы (ClusterIP, NodePort, LoadBalancer); что такое Ingress и зачем он, если уже есть Service
* ConfigMap и Secret: в чём разница и как передать конфигурацию и секреты (пароли к базе, ключи провайдеров в Kubernetes Secrets) в Spring Boot-приложение
* Пробы liveness, readiness и startup: чем отличаются, как их настроить для Spring Boot (Actuator health groups) и что будет при ошибке настройки
* Requests и limits ресурсов: почему под получает OOMKilled или CPU throttling и как настроить JVM под лимиты контейнера (MaxRAMPercentage)
* Rolling update в Kubernetes: maxSurge и maxUnavailable, откат через kubectl rollout undo
* Масштабирование в Kubernetes: число реплик и HorizontalPodAutoscaler
* Graceful shutdown Spring Boot-сервиса в Kubernetes: SIGTERM, server.shutdown=graceful, preStop и terminationGracePeriodSeconds
* StatefulSet: чем отличается от Deployment и когда нужен
* Как задеплоить Java-сервис в Kubernetes: образ, манифесты или Helm-чарт с values, конфигурация, пробы, ресурсы
* Deployment в Kubernetes: Load Balancer/Ingress и WAF на edge, namespaces core и data, реплики сервисов
* Данные и наблюдаемость в кластере: primary + replica БД, object storage, метрики, логи, трейсы, алертинг
* Сервисы в Kubernetes в трёх зонах; Schedule Sync Job по расписанию с перезапуском на другом узле
* Диагностика через kubectl: get pods, logs, exec в под брокера
