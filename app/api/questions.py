from fastapi import APIRouter, Depends, HTTPException
import random
from app.models.Question import Question
from app.models.AnswerSubmission import FirstRoundSubmission, CandidateResult
from app.repositories.collection_deps import get_questions_collection, get_results_collection

router = APIRouter()

@router.get("/questions")
async def get_questions(
        size: int = 25,
        collection = Depends(get_questions_collection)
):
    """Retrieve a question by its ID."""
    result = await collection.find().to_list(length=100)
    questions = [Question(**doc).model_dump(exclude={"correct_option"}) for doc in result]
    random.shuffle(questions)
    return questions[:size]

@router.post("/submit_answers")
async def submit_answers(
    submission: FirstRoundSubmission,
    collection = Depends(get_questions_collection),
    results_collection = Depends(get_results_collection)
):
    """Submit answers for the first round of questions and get a score."""
    score = 0
    for answer in submission.answers:
        question_doc = await collection.find_one({"question_id": answer.question_id})
        if not question_doc:
            raise HTTPException(status_code=404, detail=f"Question ID {answer.question_id} not found.")
        question = Question(**question_doc)
        is_correct = (answer.selected_option == question.correct_option)
        if is_correct:
            score += 1
    percentage = score / len(submission.answers) * 100 if submission.answers else 0.0
    candidata_result = CandidateResult(
        candidate_id=submission.candidate_id,
        first_round_score=score,
        first_round_percentage=percentage,
        total_questions=len(submission.answers),
        first_round_answers=submission.answers
    )
    await results_collection.insert_one(candidata_result.model_dump(by_alias=True, exclude=["id"]))

    if percentage >= 50.0:
        return {
            "status": "passed",
            "allow_to_second_round": True,
            "message": "Congratulations! You have passed the first round."
        }
    else:
        return {
            "status": "failed",
            "allow_to_second_round": False,
            "message": "Unfortunately, you did not pass the first round."
        }


