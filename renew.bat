@echo off
cd %~dp0
docker-compose down --rmi all
docker system prune --force
docker volume prune --force
docker-compose pull
docker-compose up -d
exit /b 0