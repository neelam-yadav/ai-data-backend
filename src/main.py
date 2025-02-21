from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.common import Base, engine
from src.routers import pipelines, users, config, workflow, evaluation

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Configure CORS
origins = [
    "http://localhost:5173",  # React development server
    "http://127.0.0.1:5173", # Alternate localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(pipelines.router, prefix="/api/pipelines", tags=["pipelines"])
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["workflow"])
app.include_router(evaluation.router, prefix="/api/evaluate", tags=["evaluation"])


import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# from src.common import load_config
# from src.workflows import run_data_ingestion, data_processing_pipeline
#
# def main():
#     # Load configuration
#     config = load_config("config/config.json")
#
#     # Run the data pipeline
#     # run_data_ingestion(config)
#
#     # Run the data processing pipeline
#     data_processing_pipeline(config)
#
# if __name__ == "__main__":
#     main()
