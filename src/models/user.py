from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.common import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Relationship with pipelines
    pipelines = relationship("Pipeline", back_populates="user", lazy="selectin")
