from pydantic import BaseModel
from typing import List

class CodeEvaluationRequest(BaseModel):
    question: str
    code: str

class CodeEvaluationResponse(BaseModel):
    evaluation: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    code: str
    history: List[ChatMessage]

class ChatResponse(BaseModel):
    evaluation: str
