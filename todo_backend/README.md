# Todo Backend (FastAPI + SQLite)

A simple FastAPI backend providing CRUD and completion endpoints for todo tasks, persisted in a local SQLite database.

## Endpoints

- POST /tasks — create a task
- GET /tasks — list tasks
- GET /tasks/{id} — get a task by id
- PUT /tasks/{id} — update task fields (title, description, completed)
- PATCH /tasks/{id}/complete — mark task as completed
- DELETE /tasks/{id} — delete a task
- GET / — health check

OpenAPI docs available at `/docs` and `/openapi.json`.

## Running locally

1. Install dependencies:
   - Using pip: `pip install -r requirements.txt`

2. Configure environment (optional but recommended):
   - Copy `.env.example` to `.env`
   - Set `DATABASE_URL` if you want to override the default SQLite path (see below)

3. Start the server (from the `todo_backend` directory):
   - `uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload`

4. Visit:
   - Docs: http://localhost:3001/docs
   - Health: http://localhost:3001/

## Database

- By default, uses a local SQLite file `todo.db` in the backend working directory.
- To customize the database location, set the `DATABASE_URL` environment variable to a valid SQLAlchemy SQLite URL.
  - Relative/local file example: `sqlite:///./data/todo.db`
  - Absolute path example (recommended when pointing to an external/shared database file): `sqlite:////absolute/path/to/myapp.db`
- When integrating with the separate database container, point `DATABASE_URL` to the absolute file path of the SQLite database provided by that container (e.g., from its `db_connection.txt`). Do not hardcode paths—use the value provided by the environment or that file.

## Environment variables

- `DATABASE_URL` (optional): SQLAlchemy-style database URL. Defaults to `sqlite:///./todo.db` if unset.
  - See `.env.example` for reference, and create a `.env` file locally when needed.

## Regenerate OpenAPI spec (stored in interfaces/openapi.json)

Run:
```
python -m src.api.generate_openapi
```

This imports the app and writes the schema into `interfaces/openapi.json`.
