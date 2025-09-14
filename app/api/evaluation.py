from fastapi import APIRouter

from app.models.evaluation import CodeEvaluationResponse, CodeEvaluationRequest
from app.services.ollama_service import evaluate_code

code_evaluation_router = APIRouter()

@code_evaluation_router.post("/evaluate", response_model=CodeEvaluationResponse)
async def evaluate_python_code(request: CodeEvaluationRequest):
    evaluation = evaluate_code(request.question,request.code)
    return CodeEvaluationResponse(evaluation=evaluation)