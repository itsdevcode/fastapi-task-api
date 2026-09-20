from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(250), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime|None] = mapped_column(DateTime, nullable=True,  default=None)
    
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")