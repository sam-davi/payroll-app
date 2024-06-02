# payroll-app
 
to execute with correct ENV variables

powershell:
    powershell -Command { $env:ENV="dev"; python manage.py runserver }
cmd:
    set ENV=dev
    py manage.py runserver

.env files should contain the following variables:
    SECRET_KEY=
    DEBUG=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=

.env files must be in backend directory (where manage.py is located)
    .env.prod # production settings
    .env.staging # staging settings
    .env.dev # development settings
