from typing import List

from pydantic import BaseModel

from app.models.base import BaseMongoModel


class Option(BaseModel):
    option:str # A, B, C, D
    option_text:str

class Question(BaseMongoModel):
    question_id: int
    question_text: str
    options: List[Option]
    correct_option: str # A, B, C, D

