# Football World Cup 2026 Data Pipeline 🏆

ETL пайплайн для сбора и анализа статистики матчей Чемпионата Мира по футболу.

## Архитектура
football-data.org API → Python → PostgreSQL → dbt → Metabase
↑
Airflow

## Стек технологий
- **Python** — сбор данных из API
- **PostgreSQL** — хранение данных
- **Apache Airflow** — автоматический запуск пайплайна каждый день
- **dbt** — трансформация сырых данных в аналитические модели
- **Metabase** — визуализация и дашборды
- **Docker** — контейнеризация

## Что делает пайплайн

1. Забирает данные матчей ЧМ из football-data.org API
2. Сохраняет сырые данные в PostgreSQL (таблица `matches`)
3. dbt трансформирует данные в `analytics.team_stats`
4. Airflow запускает пайплайн автоматически каждый день
5. Metabase показывает статистику на дашборде

## Запуск
1. Клонируй репозиторий
2. Создай `.env` файл с токеном API и данными БД
3. Запусти Docker: `docker-compose up`
4. Запусти dbt: `dbt run`