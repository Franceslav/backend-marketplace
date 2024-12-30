from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)  # Уникальный email
    hashed_password = Column(String, nullable=False)  # Хэшированный пароль
    is_active = Column(Boolean, default=True)  # Состояние аккаунта (активен/неактивен)
    is_admin = Column(Boolean, default=False)  # Администраторская роль
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата регистрации
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Дата последнего обновления


