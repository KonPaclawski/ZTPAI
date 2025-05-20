# ZTPAI
npm install --save @fortawesome/react-fontawesome @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons
docker-compose exec backend python manage.py makemigrations --empty backend
docker-compose exec backend python manage.py migrate --run-syncdb
