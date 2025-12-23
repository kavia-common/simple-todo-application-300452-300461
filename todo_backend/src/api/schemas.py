from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., description="Short title of the task", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Optional detailed description of the task")


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Updated title", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Updated description")
    completed: Optional[bool] = Field(None, description="Updated completion flag")


class TaskOut(BaseModel):
    id: int = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Short title of the task")
    description: Optional[str] = Field(None, description="Detailed description")
    completed: bool = Field(..., description="Whether the task is completed")
    created_at: str = Field(..., description="Creation timestamp (UTC)")
    updated_at: str = Field(..., description="Last update timestamp (UTC)")

    class Config:
        from_attributes = True
