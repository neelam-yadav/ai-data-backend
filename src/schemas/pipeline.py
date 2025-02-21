from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from src.schemas.user import UserResponseLite


class PipelineBase(BaseModel):
    name: str
    description: Optional[str]
    data_sources: List[Dict]
    ingestion_config: Dict = Field(default_factory=dict)
    processing_config: Dict


class PipelineCreate(PipelineBase):
    pass


class Pipeline(PipelineBase):
    id: int
    user: Optional[UserResponseLite]  # Updated to avoid recursion

    class Config:
        orm_mode = True


class PipelineResponseLite(PipelineBase):
    id: int

    class Config:
        orm_mode = True
