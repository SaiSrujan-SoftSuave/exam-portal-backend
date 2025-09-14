from fastapi import APIRouter

from app.api import questions

router = APIRouter()

router.include_router(questions.router, tags=["questions"],prefix="/first_round")