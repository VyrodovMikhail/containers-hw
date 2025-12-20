# lab4:

# Развертывание сервиса на Kubernetes

Этот набор манифестов разворачивает Flask приложение с PostgreSQL базой данных на Kubernetes.

## Структура

- `configmap.yml` - ConfigMap с конфигурацией приложения
- `secret.yml` - Secret с учетными данными PostgreSQL
- `postgres-deployment.yml` - Deployment для PostgreSQL
- `app-deployment.yml` - Deployment для Flask приложения (с кастомным образом)
- `app-service.yml` - Service для Flask приложения

## Развертывание

### Ручное развертывание

1. Убедимся, что Minikube запущен:
```bash
minikube status
# Если не запущен:
minikube start
```
2. Соберем Docker образ для приложения:
```bash
docker build -f init_db_Dockerfile -t container_app:init-latest .
docker build -f good_Dockerfile -t container_app:latest .
```

4. Применим манифесты в правильном порядке:
```bash
cd lab4
kubectl apply -f configmap.yml
kubectl apply -f secret.yml
kubectl apply -f postgres-deployment.yml
kubectl apply -f app-deployment.yml
kubectl apply -f app-service.yml
```

5. Проверим статус подов:
```bash
kubectl get pods
kubectl get services
```

6. Дождемся готовности подов:
```bash
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s
kubectl wait --for=condition=ready pod -l app=flask-app --timeout=120s
```

7. Получим доступ к приложению:
```bash
minikube service app-service
```

## Особенности реализации

- **2 Deployment**: `postgres-deployment` и `app-deployment`
- **Кастомный образ**: `app-deployment` использует образ`, собранный из Dockerfile
- **Init-контейнер**: `app-deployment` содержит init-контейнер для инициализации БД
- **Volumes**: 
  - `postgres-deployment` использует PersistentVolumeClaim
  - `app-deployment` использует emptyDir volume
- **ConfigMap и Secret**: используются для конфигурации и секретов
- **Пробы**: оба Deployment содержат liveness и readiness пробы

