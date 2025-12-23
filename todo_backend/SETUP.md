# Setup Guide — Todo Backend

This document explains how to configure the backend to use the SQLite database file provided by the database container and how to run local previews.

## 1) Create your local environment file

Copy the example environment file and edit it as needed:

```
cp .env.example .env
```

## 2) Read the database container connection info

The database container writes its absolute SQLite file path and a ready-to-use SQLAlchemy connection string to:

```
simple-todo-application-300452-300463/database/db_connection.txt
```

Open that file and locate one of the following lines:
- Connection string: sqlite:////home/.../simple-todo-application-300452-300463/database/myapp.db
- File path: /home/.../simple-todo-application-300452-300463/database/myapp.db

Either value can be used to configure the backend:
- If you copy the Connection string value, you can paste it directly into DATABASE_URL.
- If you copy the File path value, prepend sqlite://// to form a SQLAlchemy URL.

Example from this project:
- File path: /home/kavia/workspace/code-generation/simple-todo-application-300452-300463/database/myapp.db
- DATABASE_URL to use: sqlite:////home/kavia/workspace/code-generation/simple-todo-application-300452-300463/database/myapp.db

Important:
- Use four slashes after sqlite: when specifying an absolute file path.
- Do not hardcode paths in code. Keep this value in your .env or environment.

## 3) Set DATABASE_URL for the backend

Edit the .env file in simple-todo-application-300452-300461/todo_backend and set DATABASE_URL to the absolute-path form from step 2. For example:

```
# .env
DATABASE_URL=sqlite:////home/kavia/workspace/code-generation/simple-todo-application-300452-300463/database/myapp.db
```

If DATABASE_URL is not set, the backend defaults to:
```
sqlite:///./todo.db
```

## 4) Install dependencies and run the backend preview

From the todo_backend directory:

```
pip install -r requirements.txt
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

Open:
- Docs: http://localhost:3001/docs
- Health: http://localhost:3001/

## 5) Optional: Run the database viewer preview

The database container includes a simple Node.js viewer.

Steps (from simple-todo-application-300452-300463/database):

1) Ensure the sqlite.env file points to the same database file. It is created by init_db.py and should contain:
```
export SQLITE_DB="/home/kavia/workspace/code-generation/simple-todo-application-300452-300463/database/myapp.db"
```

2) Load the environment for the viewer (current shell session):
```
source db_visualizer/sqlite.env
```

3) Install and start the viewer:
```
cd db_visualizer
npm install
npm start
```

Viewer runs at:
- http://localhost:3000

## 6) Quick verification

- Backend: GET http://localhost:3001/ should return {"message":"Healthy"}.
- Tasks: Visit http://localhost:3001/docs and try the /tasks endpoints.
- Database viewer (optional): Visit http://localhost:3000 and explore tables.

Troubleshooting:
- If you see “SQLite database file not found” in the viewer, confirm SQLITE_DB matches the myapp.db absolute path.
- If the backend can’t open the database, confirm DATABASE_URL uses sqlite://// with an absolute path and that the file exists.
