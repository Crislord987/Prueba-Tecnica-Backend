from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from typing import Optional
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

#Paginada
def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status_filter: Optional[TaskStatus] = None
) -> tuple[list[Task], int]:
    #Filtrado opcional por status
    #Regresa lista con las tareas y cuantas hay
    query = db.query(Task)
    
    #Filtro
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    # Obtener total
    total = query.count()
    
    # Resultados paginados y ordenados por fecha de creacion
    tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    return tasks, total


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Task:
    db_task = get_task(db, task_id)
    
    #Actualiza campos proporcionados    (solo los proporcionados)
                                                #|
    update_data = task_update.model_dump(exclude_unset=True)
    #Elimina datos no proporcionados
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    
    return db_task


def delete_task(db: Session, task_id: int) -> None:
    db_task = get_task(db, task_id)
    
    db.delete(db_task)
    db.commit()
