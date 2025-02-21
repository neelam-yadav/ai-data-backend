from pydantic import BaseModel

class MongoDBConfig(BaseModel):
    host: str
    port: int

class QdrantConfig(BaseModel):
    url: str

class ConfigCreate(BaseModel):
    mongo_db: MongoDBConfig
    qdrant_db: QdrantConfig

class ConfigResponse(BaseModel):
    id: int
    mongo_db: MongoDBConfig
    qdrant_db: QdrantConfig

    class Config:
        orm_mode = True
