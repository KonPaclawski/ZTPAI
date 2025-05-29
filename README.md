# ZTPAI - Aplikacja do zarządzania budżetem
Projekt pozwala na zarządzanie swoim budżetem
Pozwala ona na zarządzanie osobistym budżetem, umożliwiając śledzenie wydatków, użytkownicy mogą tworzyć kategorie wydatków ich tytuły, cena, następną datę zapłaty. 

## Instalacja  
1. **Sklonuj repozytorium:**  
   ```bash
   git clone  https://github.com/KonPaclawski/ZTPAI.git <nazwa_folderu>
   ```
2. **Uruchom aplikację w Dockerze:**  
   ```bash
   docker-compose up --build
   ```
3. **Skonfiguruj bazę danych:**  
    ```bash
    Jezeli baza nie jest utworzona to trzeba wejsc na ten adres
    http://localhost:5050/browser/ zalogowac sie na te dane
    email: admin@admin.com
    password: admin
    Dodac serwer
    name: db
    localhost: db
    username: admin
    password: admin
    dodac nowa baza danych
    name: db
    i w terminalu zrobic migracje
    docker-compose exec backend python manage.py makemigrations backend
    docker-compose exec backend python manage.py migrate
    ```
   - 
4. **Otwórz aplikację w przeglądarce:**  
   ```
   http://localhost:3000/login
   ```

## Schemat architektury
```bash
Schemat architektury (opisowy)
Frontend (React)

Interfejs użytkownika do logowania, rejestracji oraz zarządzania budżetem i wydatkami

Komunikacja z backendem za pomocą REST API (Axios)

Backend (Django)

REST API odpowiedzialne za logikę biznesową, autoryzację (JWT w cookies), zarządzanie użytkownikami i danymi budżetowymi

Dokumentacja API generowana automatycznie (Swagger, Redoc)

Baza danych (PostgreSQL):Przechowywanie danych użytkowników, budżetów, kategorii i płatności

Docker: Konteneryzacja całego środowiska (frontend, backend, baza danych) dla łatwego uruchamiania i skalowania

```
## Technologie

```bash
Frontend (React) - bogaty ekosystem (React Router, Axios)
Backend (Django) - umozliwia łatwą autoryzację i zarządzanie użytkownikami
Baza Danych (postgreSQL) - dobrze integruje się z Django i jest szeroko wspierany.
Docker
```
## Testowanie 
```bash 
docker-compose exec backend python manage.py test backend.tests.test_register
```