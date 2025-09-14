from typing import List

from pydantic import BaseModel

from app.models.base import BaseMongoModel

class AnswerSubmission(BaseModel):
    question_id: int
    selected_option: str

class FirstRoundSubmission(BaseModel):
    candidate_id: int
    answers: List[AnswerSubmission]



class CandidateResult(BaseMongoModel):
    candidate_id: int = 0
    first_round_score: int = 0
    first_round_percentage: float = 0.0
    total_questions: int = 0
    first_round_answers: List[AnswerSubmission]
    second_round_score: int = 0
    second_round_percentage: float = 0.0
    second_round_answers: List[AnswerSubmission] = None
