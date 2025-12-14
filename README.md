# lab2

## docker-compose
```
docker compose up --build
```
Создаются три сервиса:
* db: Postgres DB
* init-db: Создание таблицы data и заполнение начальными значениями
* app: основное приложение c Flask

Порты и креды вынесены в файл `.env`.

Приложение:
- `/save-to-db` — читает `/app/data/example.txt` из volume и сохраняет содержимое в таблицу `data` в Postgres.
- `/db-rows` — выводит сохраненные строки.

## Ответы на вопросы
1. **Можно ли ограничивать ресурсы (например, память или CPU) для сервисов в docker-compose.yml? Если нет, то почему,
   если да, то как?**
    - Да, можно. Например:
   ```yaml
   services:
     app:
       resources:
         limits:
           cpus: 500m
           memory: 512M
         reservations:
           cpus: 500m
           memory: 128M
   ```

2. **Как можно запустить только определенный сервис из docker-compose.yml, не запуская остальные**
- Запуск одного сервиса: передать его имя в команду, например `docker compose up app` или одноразово `docker compose run app`.