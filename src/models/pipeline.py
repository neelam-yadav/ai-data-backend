from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.common import Base

class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    data_sources = Column(JSON, nullable=False)  # JSONB for data sources
    ingestion_config = Column(JSON, nullable=False, default={})  # JSON for ingestion config
    processing_config = Column(JSON, nullable=False, default={})  # JSONB for processing config

    # Relationship with user
    user = relationship("User", back_populates="pipelines", lazy="selectin")
