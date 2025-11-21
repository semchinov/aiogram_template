"""
Database models example using SQLAlchemy (optional).
This is a basic example showing how to integrate a database.
"""
from datetime import datetime
from typing import Optional

# Note: These are example models. To use them, install sqlalchemy and aiosqlite:
# pip install sqlalchemy aiosqlite

# Uncomment the following to use database models:
"""
from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    '''User model for storing user information.'''
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
"""
