from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

class TestCase(BaseModel):
    input: str
    expected_output: str

class CodeExecutionRequest(BaseModel):
    code: str
    language: str
    test_cases: List[TestCase]

class TestResult(BaseModel):
    passed: bool
    input: str
    expected: str
    actual: str
    is_hidden: bool = False

@router.post("/execute_code")
async def execute_code(request: CodeExecutionRequest) -> List[TestResult]:
    # This is a mock implementation. In a real scenario, you would send the code
    # to a code execution engine (e.g., Judge0, Sphere Engine, or a custom sandbox).
    
    results: List[TestResult] = []

    if request.language == "javascript":
        # Simulate JavaScript execution
        for tc in request.test_cases:
            # Mock logic: randomly pass/fail tests
            passed = True # random.choice([True, False])
            actual_output = tc.expected_output if passed else "mock_error_output"
            results.append(TestResult(
                passed=passed,
                input=tc.input,
                expected=tc.expected_output,
                actual=actual_output,
                is_hidden=False
            ))
    elif request.language == "sql":
        # Simulate SQL execution
        for tc in request.test_cases:
            # Mock logic: randomly pass/fail tests
            passed = True # random.choice([True, False])
            actual_output = tc.expected_output if passed else "mock_error_output"
            results.append(TestResult(
                passed=passed,
                input=tc.input,
                expected=tc.expected_output,
                actual=actual_output,
                is_hidden=False
            ))
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")

    return results
