from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from src.common.db import Base

class Config(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    mongo_db = Column(JSONB, nullable=False)  # Use JSONB for structured data
    qdrant_db = Column(JSONB, nullable=False)
