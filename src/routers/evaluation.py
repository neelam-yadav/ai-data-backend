from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.common.db import get_db
from src.services import evaluate_embeddings, test_retrieval, optimize_prompt, cluster_embeddings, benchmark_embeddings

router = APIRouter()

@router.get("/evaluate-embeddings/{pipeline_id}")
def evaluate_embeddings_api(pipeline_id: int, db: Session = Depends(get_db)):
    """Evaluates embedding quality for AI readiness"""
    try:
        results = evaluate_embeddings(db, pipeline_id)
        return {
            "status": "success",
            "evaluation": results
        }

    except Exception as e:
        print(f"Failed in evaluate embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-retrieval/{pipeline_id}")
def test_retrieval_api(pipeline_id: int, query: str, db: Session = Depends(get_db)):
    """Tests the AI retrieval performance"""
    try:
        results = test_retrieval(db, pipeline_id, query)
        return {"status": "success", "retrieval_evaluation": results}
    except Exception as e:
        print(f"Failed in retrieval api: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/optimize-prompt")
def optimize_prompt_api(query: str):
    """Suggests an improved prompt for AI retrieval"""
    optimized_query = optimize_prompt(query)
    return {"optimized_query": optimized_query}


@router.get("/cluster-embeddings/{pipeline_id}")
def cluster_embeddings_api(pipeline_id: int, db: Session = Depends(get_db)):
    """Clusters embeddings to test AI readiness"""
    try:
        result = cluster_embeddings(db, pipeline_id)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/benchmark-embeddings/{pipeline_id}")
def benchmark_embeddings_api(pipeline_id: int, db: Session = Depends(get_db)):
    """Benchmarks embeddings with standard datasets"""
    try:
        result = benchmark_embeddings(db, pipeline_id)
        return {"status": "success", "benchmark_results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


