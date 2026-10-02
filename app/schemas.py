from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    status: Optional[str] = "todo"
    project_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    text: str
    task_id: int
    user_id: int

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagOut(TagBase):
    id: int
    class Config:
        from_attributes = True