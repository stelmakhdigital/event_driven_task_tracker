## Последние архитектурные решения (ADR)

<!-- ADR_TABLE_START -->
| Number ADR | Data | Author | Status | Description |
|------------|------|--------|--------|-------------|
| [0008](ADRs/0008_logs.md) | 2025-07-05 | Aleksandr Maystrishin <nuclear0077@gmail.com> | Suggested | Хранение логов проекта. |
| [0007](ADRs/0007_deploy_in_kubernetes.md) | 2025-07-05 |  Dmitry Stelmakh <TG: @StelmakhDigital> | Suggested | Необходимость оркестрации 5+ микросервисов с возможностью быстрого горизонтального масштабирования |
| [0006](ADRs/0006_logs_and_telemetry.md) | 2025-07-05 |  Dmitry Stelmakh <TG: @StelmakhDigital> | Suggested | Если все же инцидент достиг свое критического значения, то важно найти его эпицентр - в этом поспособствуют логи и телеметрия запроса. |
| [0005](ADRs/0005_monitoring_and_metricks.md) | 2025-07-05 |  Dmitry Stelmakh <TG: @StelmakhDigital> | Suggested | В highload важно не допускать проблем с сервисами и разбираться с инцидентами еще до наступления критических ситуаций. Мониторинг разнообразных метрик "жизни" сервисов как раз в этом помогает. |
| [0004](ADRs/0004_cache_in_redis.md) | 2025-07-05 |  Dmitry Stelmakh <TG: @StelmakhDigital> | Suggested | Даже с использованием шардов в БД нагрузка на нее все еще высокая. Можно использовать кеш чтобы убрать с БД "мусорные однотипные запросы" (частые запросы на получение информации > 5 RPS (например по м... |
| [0003](ADRs/0003_sharding_in_postgres.md) | 2025-07-05 |  Dmitry Stelmakh <TG: @StelmakhDigital> | Suggested | Со временем работа сервиса приведет к "разбуханию" основной таблицы с задачами (>2-3 Млн. задач в месяц) |
| [0002](ADRs/0002_kafka_main_event_bus.md) | 2025-07-05 |  Dmitry Stelmakh <TG: @StelmakhDigital> | Suggested | Одно из главных требований сервиса обработка >10K событий/час с гарантией доставки |
| [0001](ADRs/0001_fastapi_main_framework.md) | 2025-07-05 |  Dmitry Stelmakh <TG: @StelmakhDigital> | Suggested | Выбор основного фреймворка для микросервисов (в частности для `Task Service`, `API Gateway` и других сервисов) для снижения временных издержек в разработке и поддержке микросервисов |
<!-- ADR_TABLE_END -->