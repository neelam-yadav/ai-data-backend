from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.pipeline import Pipeline
from src.schemas.pipeline import PipelineCreate


def get_pipelines_by_user(db: Session, user_id: int):
    """Fetch all pipelines for a specific user."""
    pipelines = db.query(Pipeline).filter(Pipeline.user_id == user_id).all()
# Ensure ingestion_config is always a dictionary
    for pipeline in pipelines:
        if pipeline.ingestion_config is None:
            pipeline.ingestion_config = {}
    return pipelines


def get_pipeline_by_id(db: Session, pipeline_id: int):
    """Fetch pipeline details including ingestion config"""
    pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
    if not pipeline:
        print(f"Pipeline with ID {pipeline_id} not found.")
        return None
    return pipeline


def get_pipeline_data_sources(db: Session, pipeline_id: int):
    """
    Fetches data sources of a given pipeline.

    :param db: Database session
    :param pipeline_id: ID of the pipeline
    :return: List of data sources or an error message
    """
    pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()

    if not pipeline:
        return {"error": "Pipeline not found"}

    return pipeline.data_sources


def create_pipeline(db: Session, pipeline: PipelineCreate, user_id: int):
    """Create a new pipeline for a user."""
    db_pipeline = Pipeline(
        user_id=user_id,
        name=pipeline.name,
        description=pipeline.description,
        data_sources=pipeline.data_sources,
        ingestion_config=pipeline.ingestion_config,
        processing_config=pipeline.processing_config,
    )
    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline


def update_pipeline(db: Session, pipeline_id: int, pipeline: PipelineCreate, user_id: int):
    """Update an existing pipeline."""
    db_pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id, Pipeline.user_id == user_id).first()
    if not db_pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    db_pipeline.name = pipeline.name
    db_pipeline.description = pipeline.description
    db_pipeline.data_sources = pipeline.data_sources
    db_pipeline.ingestion_config = pipeline.ingestion_config
    db_pipeline.processing_config = pipeline.processing_config
    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline


def delete_pipeline(db: Session, pipeline_id: int, user_id: int):
    """Delete a pipeline by ID."""
    db_pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id, Pipeline.user_id == user_id).first()
    if not db_pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    db.delete(db_pipeline)
    db.commit()
