# Blog Platform API

FastAPI Microservice for a Mini "Bookstore" API with Search, Authentication, and File Upload, for managing a simple bookstore inventory. The system should allow authenticated users to manage books, search for them, and upload a CSV file to bulk-insert books.
User registration verification through email.
User profile image and book cover images are being stored on ImageKit. 
Package management is handled with **Poetry**.

```
Database fallback: By default, the API uses PostgreSQL (via DATABASE_URL).
If no configuration is found, it will seamlessly switch to a local SQLite file (blog_platform_api.db) 
so you can run the project immediately without extra setup.
```

---

## 📦 Requirements

- Python **3.12+**
- [Poetry](https://python-poetry.org/) (dependency management)
- PostgreSQL (or compatible database)

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/bookstore_api.git
cd bookstore_api
```

### 2️⃣ Install dependencies

- If you dont have poetry installed on your system
```
pip install poetry
poetry --version
```

- Without dev tools (production-like)

```
poetry install
```
If poetry install doesn't work, try:
```
poetry install --no-root
```
-With dev tools (ruff for formatting)
```
poetry install --with dev
```

### 3️⃣ Setup environment variables

- Create .env file in the project root
- Edit .env with your own values.
- Remove SYNC_DATABASE_URL and ASYNC_DATABASE_URL from .env and SQLite DB will initialize in root directory, otherwise add valid postgreSQL urls.

Example .env:
```
SYNC_DATABASE_URL = postgresql+psycopg2://username:password@localhost:5432/bookstore_api_db
ASYNC_DATABASE_URL = postgresql+asyncpg://username:password@localhost:5432/bookstore_api_db

SECRET_KEY = 'use "openssl rand -hex 32" to generate secret key'
ALGORITHM = HS256
TOKEN_EXPIRE_MINUTES = 60


IMAGEKIT_PRIVATE_KEY=private_Dfirf...................
IMAGEKIT_PUBLIC_KEY=public_jirnD.....................
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/url_endpoint
    
MAIL_USERNAME=example@gmail.com
MAIL_PASSWORD=**** **** **** ****
MAIL_FROM=example@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

```

### 4️⃣ Run database migrations

Alembic is used for database migrations.

- Generate a migration after making model changes:
```
poetry run alembic revision --autogenerate -m "description of changes"
```
- Apply migrations:
```
poetry run alembic upgrade head
```
- Downgrade migration (optional):
```
poetry run alembic downgrade -1
```

### 5️⃣ Start the development server

```
poetry run uvicorn app.main:app --reload
```

- On startup, FastAPI creates an admin user, admin@gmail.com - password: admin123, for first admin user.

### The initial admin user must be preconfigured in the system

You can change credentials in main.py.

- The API will be available at:

```
http://127.0.0.1:8000
```

- Swagger Docs
```
http://127.0.0.1:8000/docs
```

## 🛠 Project Structure

```
.
├── alembic/               # Database migration scripts
├── config/                # Config, security, auth
├── models/                # SQLAlchemy models
├── routes/                # Routes and endpoints
├── schemas/               # Pydantic schemas
├── main.py                # FastAPI entry point
├── utils/                 # hashing and dependencies
├── alembic.ini            # Alembic configuration
├── pyproject.toml         # Poetry dependencies
├── poetry.lock            # Locked dependency versions
├── .env.example           # Environment variable template
├── README.md              # This file
└── .gitignore             # Ignored files

```

## Utils

### Run generate_dummy_data.py file to generate 2 CSV file with custom data, one with errors. 
    
    For quick testing.

    - books_valid.csv contains accurate rows (to test /books/upload)
    - books_faulty.csv contains faulty rows
