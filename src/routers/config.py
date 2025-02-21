from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.config import ConfigCreate, ConfigResponse
from src.crud.config import get_config, create_or_update_config
from src.common.db import get_db

router = APIRouter()

@router.get("/", response_model=ConfigResponse)
def fetch_config(db: Session = Depends(get_db)):
    """Fetch the current configuration"""
    config = get_config(db)
    if not config:
        return ConfigResponse(  # Return default values to match schema
            id=0,
            mongo_db={"host": "", "port": 0},
            qdrant_db={"url": ""}
        )
    return config

@router.post("/", response_model=ConfigResponse)
def update_config(config_data: ConfigCreate, db: Session = Depends(get_db)):
    """Create or update configuration"""
    return create_or_update_config(db, config_data)
