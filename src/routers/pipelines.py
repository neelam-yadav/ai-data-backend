from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.common.db import get_db
from src.models import Pipeline as PipelineModel
from src.schemas.pipeline import Pipeline, PipelineCreate, PipelineResponseLite
from src.crud.pipeline import create_pipeline, get_pipelines_by_user, update_pipeline, delete_pipeline

router = APIRouter()

# Admin user ID (hardcoded for now)
ADMIN_USER_ID = 1


@router.post("/", response_model=Pipeline)
def save_pipeline(pipeline: PipelineCreate, db: Session = Depends(get_db)):
    """Save a new pipeline for the admin user."""
    return create_pipeline(db=db, pipeline=pipeline, user_id=ADMIN_USER_ID)


@router.get("/", response_model=list[Pipeline])
def fetch_pipelines(db: Session = Depends(get_db)):
    """Fetch all pipelines for the admin user."""
    pipelines = get_pipelines_by_user(db=db, user_id=ADMIN_USER_ID)
    # if not pipelines:
    #     raise HTTPException(status_code=404, detail="No pipelines found")
    return pipelines


@router.get("/{pipeline_id}", response_model=PipelineResponseLite)
def get_pipeline_by_id(pipeline_id: int, db: Session = Depends(get_db)):
    """Fetch a specific pipeline by ID."""
    pipeline = db.query(PipelineModel).filter(PipelineModel.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@router.put("/{pipeline_id}", response_model=Pipeline)
def update_existing_pipeline(pipeline_id: int, pipeline: PipelineCreate, db: Session = Depends(get_db)):
    """Update an existing pipeline."""
    return update_pipeline(db=db, pipeline_id=pipeline_id, pipeline=pipeline, user_id=ADMIN_USER_ID)


@router.delete("/{pipeline_id}", status_code=204)
def delete_pipeline_by_id(pipeline_id: int, db: Session = Depends(get_db)):
    """Delete a pipeline by ID."""
    delete_pipeline(db=db, pipeline_id=pipeline_id, user_id=ADMIN_USER_ID)
    return {"message": f"Pipeline with ID {pipeline_id} deleted successfully"}
