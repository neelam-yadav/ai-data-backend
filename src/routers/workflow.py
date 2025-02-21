from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.workflows import run_data_ingestion, data_processing_pipeline
from src.common.db import get_db

router = APIRouter()

@router.post("/start-ingestion/{pipeline_id}")
def start_data_ingestion(pipeline_id: int, db: Session = Depends(get_db)):
    """API to trigger data ingestion for a specific pipeline"""
    try:
        result = run_data_ingestion(db, pipeline_id)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return {"status": "success", "message": result["message"]}
    except Exception as e:
        print(f"Error in data ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start-processing/{pipeline_id}")
def start_data_processing(pipeline_id: int, db: Session = Depends(get_db)):
    """API to trigger data processing for a specific pipeline"""
    try:
        result = data_processing_pipeline(db, pipeline_id)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return {"status": "success", "message": result["message"]}
    except Exception as e:
        print(f"Error in data ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
