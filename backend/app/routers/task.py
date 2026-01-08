from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _is_project_owner(db: Session, project_id: int, user: User) -> bool:
    if user.role == "admin":
        return True
    project = db.query(Project).filter(Project.id == project_id).first()
    return bool(project and project.owner_id == user.id)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Seul admin ou owner du projet peut créer des tâches dans ce projet
    if current_user.role != "admin" and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        project_id=payload.project_id,
        assignee_id=payload.assignee_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskRead.model_validate(task)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    project_id: int | None = None,
    assigned_to_me: bool = False,
    skip: int = 0,
    limit: int = 50
):
    q = db.query(Task)

    if project_id is not None:
        # Restreindre l’accès aux tâches du projet : admin ou owner
        if not _is_project_owner(db, project_id, current_user):
            raise HTTPException(status_code=403, detail="Not allowed")
        q = q.filter(Task.project_id == project_id)
    else:
        # Sans project_id : admin voit tout.
        # Sinon: owner voit tâches de ses projets + assignee voit ses tâches.
        if current_user.role != "admin":
            q = q.join(Project, Task.project_id == Project.id).filter(
                (Project.owner_id == current_user.id) | (Task.assignee_id == current_user.id)
            )

    if assigned_to_me:
        q = q.filter(Task.assignee_id == current_user.id)

    tasks = q.offset(skip).limit(limit).all()
    return [TaskRead.model_validate(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # admin OK / owner projet OK / assignee OK
    if current_user.role != "admin":
        project = db.query(Project).filter(Project.id == task.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.owner_id != current_user.id and task.assignee_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    is_admin = current_user.role == "admin"
    is_owner = project.owner_id == current_user.id
    is_assignee = task.assignee_id == current_user.id

    if not (is_admin or is_owner or is_assignee):
        raise HTTPException(status_code=403, detail="Not allowed")

    # Owner/admin : peut tout modifier (dans ce schéma: title/desc/status/assignee_id)
    # Assignee : ne peut PAS réassigner
    if payload.assignee_id is not None and not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Assignee cannot reassign task")

    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.status is not None:
        task.status = payload.status
    if payload.assignee_id is not None:
        task.assignee_id = payload.assignee_id

    db.commit()
    db.refresh(task)
    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role != "admin" and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(task)
    db.commit()
    return None
