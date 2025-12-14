# lab3

## 1. Установка minikube
1. Предварительно установим Docker Desktop
   
2. Скачаем kubectl и minikube-installer
3. Запустим minikube командой minikube start
   
![a](lab3/img/1.jpg)

5. Проверим наличие контейнера minikube
   
![docker ps](lab3/img/2.jpg)

5. Посмотрим конфиг кластера
![](lab3/img/3.jpg)


## 2. Создаем объекты через CLI
1. Порогоним манифесты для создания объектов в кластере
   
![kubectl get тип_ресурса](lab3/img/4.jpg)

2. Проверим, что все сервисы создались

![kubectl get тип_ресурса](lab3/img/5.jpg)

3. Создадим nextcloud

Содержимое секрета скрыто

![kubectl get тип_ресурса](lab3/img/6.jpg)

![kubectl get тип_ресурса](lab3/img/7.jpg)

![kubectl get тип_ресурса](lab3/img/10.jpg)

4. Посмотрим поды и логи
![kubectl get тип_ресурса](lab3/img/8.jpg)

![kubectl get тип_ресурса](lab3/img/9.jpg)

## 3. Подключаемся извне
1. Создадим сервис специальной командой и осуществим туннелирование трафика между нодой minikube и сервисом

![kubectl get тип_ресурса](lab3/img/11.jpg)

![kubectl get тип_ресурса](lab3/img/12.jpg)

2. Установим допкомпонент dashboard для minikube

![kubectl get тип_ресурса](lab3/img/13.jpg)

## 4. Модифицируем исходные манифесты
1. Создадим манифест ```pg_secret.yml``` и перенесем туда значения POSTGRES_USER и POSTGRES_PASSWORD
```
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  labels:
    app: postgres
type: Opaque
stringData:
  POSTGRES_USER: "postgres"
  POSTGRES_PASSWORD: "my_password"
```
2. Перенесем переменные nextcloud из деплоймента в конфигмап
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: nextcloud-configmap
  labels:
    app: nextcloud
data:
  NEXTCLOUD_UPDATE: '1'
  ALLOW_EMPTY_PASSWORD: 'yes'
  POSTGRES_HOST: postgres-service
  NEXTCLOUD_TRUSTED_DOMAINS: "127.0.0.1"
  NEXTCLOUD_ADMIN_USER: "admin"
```

3. Добавим Liveness и Readiness пробы
```
        livenessProbe:
          httpGet:
            path: /status.php
            port: 80
            httpHeaders:
            - name: Host
              value: localhost
          initialDelaySeconds: 120
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /status.php
            port: 80
            httpHeaders:
            - name: Host
              value: localhost
          initialDelaySeconds: 30
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
```


## Ответы на вопросы

1. Важен ли порядок выполнения манифестов kubernetes? Почему?
   
Да, порядок выполнения манифестов Kubernetes важен, но Kubernetes сам управляет некоторыми аспектами зависимостей. В нашем примере Deployment nextcloud имеет значения, описанные в ConfigMap и Secret манифестов pg_configmap.yml, pg_secret.yml.

2. Что (и почему) произойдет, если отскейлить количество реплик postgres-deployment в 0, затем обратно в 1, после чего попробовать снова зайти на Nextcloud?

Nextcloud перестанет работать и данные могут быть потеряны, потому что PostgreSQL - stateful приложение, а не stateless.
