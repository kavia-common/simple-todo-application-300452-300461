# simple-todo-application-300452-300461

## Quickstart: Configure DATABASE_URL from the database container

The backend supports a DATABASE_URL environment variable and defaults to `sqlite:///./todo.db`. To use the shared SQLite database from the database container:

1) Locate the connection info file:
   - `../simple-todo-application-300452-300463/database/db_connection.txt`

2) Open the file and copy either:
   - The “Connection string:” line (preferred), for example:
     `sqlite:////home/kavia/workspace/code-generation/simple-todo-application-300452-300463/database/myapp.db`
   - Or the “File path:” line, for example:
     `/home/kavia/workspace/code-generation/simple-todo-application-300452-300463/database/myapp.db`
     If you use the file path, prepend `sqlite:////` when setting DATABASE_URL.

3) Create/update the backend .env:
   - Path: `todo_backend/.env`
   - Example:
     ```
     DATABASE_URL=sqlite:////home/kavia/workspace/code-generation/simple-todo-application-300452-300463/database/myapp.db
     ```

For more detail, see `todo_backend/SETUP.md`.

## Preview: Run the backend locally

From `todo_backend`:

```
pip install -r requirements.txt
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

Open:
- Docs: http://localhost:3001/docs
- Health: http://localhost:3001/

## Optional Preview: Database viewer

From `simple-todo-application-300452-300463/database`:

1) Ensure `db_visualizer/sqlite.env` points to your `myapp.db` (created by init_db.py). Example:
```
export SQLITE_DB="/home/kavia/workspace/code-generation/simple-todo-application-300452-300463/database/myapp.db"
```

2) Load env, install, and run:
```
source db_visualizer/sqlite.env
cd db_visualizer
npm install
npm start
```

Viewer:
- http://localhost:3000