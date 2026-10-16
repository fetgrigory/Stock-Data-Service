from sqlalchemy import Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


# Defining the 'users' table structure
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
