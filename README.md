# ZTPAI
docker-compose exec backend python manage.py makemigrations --empty backend
docker-compose exec backend python manage.py migrate --run-syncdb