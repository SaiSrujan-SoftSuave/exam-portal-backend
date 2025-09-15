from fastapi import APIRouter

from app.api import questions, compiler, image_upload
from app.api.evaluation import code_evaluation_router

router = APIRouter()

router.include_router(questions.router, tags=["questions"],prefix="/first_round")
router.include_router(code_evaluation_router, prefix="/code_evaluation", tags=["code_evaluation"])
router.include_router(compiler.router, tags=["compiler"], prefix="/compiler")
router.include_router(image_upload.router, tags=["image_upload"], prefix="/image")