# Setup Guide — Todo Backend

This document describes how to configure environment variables for running the FastAPI backend, especially when using a shared SQLite database file from a separate database container.

## 1) Create your local environment file

Copy the example environment file and edit it as needed:

```
cp .env.example .env
```

## 2) Configure the database URL

The application reads the SQLAlchemy-style database URL from the `DATABASE_URL` environment variable. If it is not set, it defaults to:

```
sqlite:///./todo.db
```

To point the backend to an external/shared SQLite database file (e.g., from a database container), set `DATABASE_URL` to the absolute path SQLite URL form:

```
DATABASE_URL=sqlite:////absolute/path/to/myapp.db
```

Notes:
- Use four slashes after `sqlite:` when specifying an absolute file path.
- Do not hardcode paths in code. Keep this value in your `.env` or environment.

If the database container provides a `db_connection.txt` file with the absolute database path, use that path with the `sqlite:////` prefix as shown above.

## 3) Install and run

Install dependencies and start the server (from `todo_backend`):

```
pip install -r requirements.txt
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

Open:
- Docs: http://localhost:3001/docs
- Health: http://localhost:3001/
