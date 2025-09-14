from fastapi import APIRouter

from app.api import questions
from app.api.evaluation import code_evaluation_router

router = APIRouter()

router.include_router(questions.router, tags=["questions"],prefix="/first_round")
router.include_router(code_evaluation_router, prefix="/code_evaluation", tags=["code_evaluation"])