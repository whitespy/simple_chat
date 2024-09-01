# Simple chat

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## How to run project locally

### 1 Install Python 3.12 and setup virtual environment

### 2 Install project requirements

```bash
python -m pip install -r requirements/base.txt
```

### 3 Create .env file and add SECRET_KEY

```bash
echo "SECRET_KEY=$(openssl rand -hex 40)" > .env
```

### 4 Apply database migrations

```bash
python manage.py migrate
```

### 5 Load test users from fixture

```bash
python manage.py loaddata fixtures/users/initial_data.json
```

### 6 Run local server

```bash
python manage.py runserver
```

### 7 Open Swagger to check out API endpoints

```bash
sensible-browser http://127.0.0.1:8000/api/docs/
```

## Test user credentials

| username | password        |
|----------|-----------------|
| `admin`  | xhSvIBITTYmIBww |
| `user1`  | xhSvIBITTYmIBww |
| `user2`  | xhSvIBITTYmIBww |
