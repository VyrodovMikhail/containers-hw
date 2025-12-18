
echo "Building Docker images..."

VERSION=$(date +%Y%m%d-%H%M)

docker build -f init_db_Dockerfile -t container_app:init-latest .
docker build -f good_Dockerfile -t container_app:latest .

minikube image load container_app:init-1
minikube image load container_app:1

kubectl set image deployment/app-deployment \
  app-container=container_app:latest \
  init-db=container_app:init-latest

kubectl delete deployment app-deployment
kubectl delete deployment postgres-deployment
kubectl service deployment app-service

kubectl apply -f lab4/app-secret.yml
kubectl apply -f lab4/app-deployment.yml
kubectl apply -f lab4/postgres-deployment.yml
kubectl apply -f lab4/app-deployment.yml
kubectl apply -f lab4/app-service.yml

kubectl wait --for=condition=available --timeout=300s deployment/postgres-deployment
kubectl wait --for=condition=available --timeout=300s deployment/app-deployment