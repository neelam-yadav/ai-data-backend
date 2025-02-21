from src.models.config import Config
from src.schemas.config import ConfigCreate
from sqlalchemy.orm import Session

def get_config(db: Session):
    return db.query(Config).first()

def create_or_update_config(db: Session, config_data: ConfigCreate):
    config = db.query(Config).first()
    if config:
        # Update existing configuration
        config.mongo_db = config_data.mongo_db.dict()
        config.qdrant_db = config_data.qdrant_db.dict()
    else:
        # Create new configuration
        config = Config(
            mongo_db=config_data.mongo_db.dict(),
            qdrant_db=config_data.qdrant_db.dict(),
        )
        db.add(config)
    db.commit()
    db.refresh(config)
    return config
