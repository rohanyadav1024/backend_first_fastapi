from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship

from .database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, index=True)
    email = Column(String(50), nullable=False,unique=True, index=True)
    password = Column(String(500), nullable=False)
    isactive = Column(Boolean, nullable=False, default=True)

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50), nullable=False, index=True)
    content = Column(String(100), nullable=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
    published = Column(Boolean, default=True, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Users")

class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True, nullable=False)