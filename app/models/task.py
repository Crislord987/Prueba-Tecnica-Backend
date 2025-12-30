from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, Index
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class TaskStatus(str, enum.Enum):
    #Enumeraciaon del estado de Task
    PENDING = "pending"
    IN_PROCES = "in_progress"
    DONE = "done"


class Task(Base):
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus, values_callable=lambda x: [e.value for e in x]), default=TaskStatus.PENDING, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # indice compuesto que Filtra por status y ordena por fecha
    __table_args__ = (
        Index('ix_tasks_status_created_at', 'status', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
