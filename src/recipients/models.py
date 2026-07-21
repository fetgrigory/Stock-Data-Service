from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


# Defining the 'recipients' table structure
class Recipient(Base):
    __tablename__ = "recipients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
