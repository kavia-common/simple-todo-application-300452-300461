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

2. Start the server (from the `todo_backend` directory):
   - `uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload`

3. Visit:
   - Docs: http://localhost:3001/docs
   - Health: http://localhost:3001/

## Database

- Uses a local SQLite file `todo.db` in the backend working directory by default.
- To customize the database location, set `DATABASE_URL` environment variable (e.g., `sqlite:///./data/todo.db`).

## Environment variables

- DATABASE_URL (optional): SQLAlchemy-style database URL. Defaults to `sqlite:///./todo.db`.

See `.env.example` for reference.

## Regenerate OpenAPI spec (stored in interfaces/openapi.json)

Run:
```
python -m src.api.generate_openapi
```

This imports the app and writes the schema into `interfaces/openapi.json`.
