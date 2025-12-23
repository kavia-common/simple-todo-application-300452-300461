from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.api.db import get_db_session
from src.api.schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def row_to_task_out(row) -> TaskOut:
    """Convert a SQLAlchemy Row to TaskOut."""
    return TaskOut(
        id=row.id,
        title=row.title,
        description=row.description,
        completed=bool(row.completed),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Create a new task with a title and optional description.",
    responses={
        201: {"description": "Task created"},
        400: {"description": "Invalid input"},
    },
)
def create_task(payload: TaskCreate, db: Session = Depends(get_db_session)) -> TaskOut:
    """Create a new task."""
    insert_stmt = text(
        """
        INSERT INTO tasks (title, description, completed, created_at, updated_at)
        VALUES (:title, :description, 0, datetime('now'), datetime('now'))
        """
    )
    db.execute(insert_stmt, {"title": payload.title, "description": payload.description})

    # Fetch the created row (SQLite's last_insert_rowid())
    row = db.execute(text("SELECT last_insert_rowid() as id")).mappings().first()
    new_id = row["id"]

    task_row = db.execute(
        text("SELECT id, title, description, completed, created_at, updated_at FROM tasks WHERE id = :id"),
        {"id": new_id},
    ).mappings().first()

    return row_to_task_out(task_row)


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[TaskOut],
    summary="List tasks",
    description="Retrieve a list of all tasks.",
)
def list_tasks(db: Session = Depends(get_db_session)) -> List[TaskOut]:
    """List all tasks."""
    rows = db.execute(
        text("SELECT id, title, description, completed, created_at, updated_at FROM tasks ORDER BY id DESC")
    ).mappings().all()
    return [row_to_task_out(r) for r in rows]


# PUBLIC_INTERFACE
@router.get(
    "/{task_id}",
    response_model=TaskOut,
    summary="Get task",
    description="Retrieve a single task by its ID.",
    responses={404: {"description": "Task not found"}},
)
def get_task(
    task_id: int = Path(..., description="ID of the task to retrieve", ge=1),
    db: Session = Depends(get_db_session),
) -> TaskOut:
    """Get a task by ID."""
    row = db.execute(
        text("SELECT id, title, description, completed, created_at, updated_at FROM tasks WHERE id = :id"),
        {"id": task_id},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return row_to_task_out(row)


# PUBLIC_INTERFACE
@router.put(
    "/{task_id}",
    response_model=TaskOut,
    summary="Update task",
    description="Replace the task's content (title/description/completed).",
    responses={404: {"description": "Task not found"}},
)
def update_task(
    payload: TaskUpdate,
    task_id: int = Path(..., description="ID of the task to update", ge=1),
    db: Session = Depends(get_db_session),
) -> TaskOut:
    """Update a task by replacing provided fields. At least one field should be provided."""
    # Verify existence
    exists = db.execute(text("SELECT id FROM tasks WHERE id = :id"), {"id": task_id}).first()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if payload.title is None and payload.description is None and payload.completed is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided to update")

    update_fields = []
    params = {"id": task_id}
    if payload.title is not None:
        update_fields.append("title = :title")
        params["title"] = payload.title
    if payload.description is not None:
        update_fields.append("description = :description")
        params["description"] = payload.description
    if payload.completed is not None:
        update_fields.append("completed = :completed")
        params["completed"] = 1 if payload.completed else 0

    update_fields.append("updated_at = datetime('now')")

    stmt = text(f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = :id")
    db.execute(stmt, params)

    row = db.execute(
        text("SELECT id, title, description, completed, created_at, updated_at FROM tasks WHERE id = :id"),
        {"id": task_id},
    ).mappings().first()
    return row_to_task_out(row)


# PUBLIC_INTERFACE
@router.patch(
    "/{task_id}/complete",
    response_model=TaskOut,
    summary="Mark task as completed",
    description="Mark an existing task as completed.",
    responses={404: {"description": "Task not found"}},
)
def complete_task(
    task_id: int = Path(..., description="ID of the task to mark as completed", ge=1),
    db: Session = Depends(get_db_session),
) -> TaskOut:
    """Mark a task as completed."""
    # Verify existence
    exists = db.execute(text("SELECT id FROM tasks WHERE id = :id"), {"id": task_id}).first()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.execute(
        text("UPDATE tasks SET completed = 1, updated_at = datetime('now') WHERE id = :id"),
        {"id": task_id},
    )
    row = db.execute(
        text("SELECT id, title, description, completed, created_at, updated_at FROM tasks WHERE id = :id"),
        {"id": task_id},
    ).mappings().first()
    return row_to_task_out(row)


# PUBLIC_INTERFACE
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task by its ID.",
    responses={404: {"description": "Task not found"}, 204: {"description": "Task deleted"}},
)
def delete_task(
    task_id: int = Path(..., description="ID of the task to delete", ge=1),
    db: Session = Depends(get_db_session),
) -> None:
    """Delete a task by ID."""
    result = db.execute(text("DELETE FROM tasks WHERE id = :id"), {"id": task_id})
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # 204 No Content
    return None
