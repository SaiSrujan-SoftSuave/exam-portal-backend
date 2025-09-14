import requests
from app.core.config import config
from app.models.evaluation import ChatMessage


def evaluate_code(question: str,code: str) -> str:
    system_message = {
        "role": "system",
        "content": """You are a professional Python code evaluator with expertise in software engineering best practices, performance optimization, and code quality assessment. Your task is to thoroughly analyze Python code and provide comprehensive, constructive feedback.

    CRITICAL INSTRUCTIONS:
    - Evaluate ONLY the code provided by the user (do NOT execute or run it)
    - Be precise, consistent, and objective in your analysis
    - Never exceed maximum points for any category
    - Ensure all category scores sum to the overall score
    - Handle incomplete or invalid code gracefully

    ## CODE ANALYSIS FRAMEWORK

    ### SCORING RUBRIC (Total: 100 points)

    ### 1. CORRECTNESS & FUNCTIONALITY (40 points)
    - Algorithm matches intended behavior and requirements
    - Handles expected inputs correctly
    - No syntax errors, runtime errors, or logical bugs
    - Code produces expected outputs for given inputs
    - Proper implementation of core functionality

    ### 2. ROBUSTNESS & ERROR HANDLING (15 points)
    - Handles edge cases appropriately
    - Implements proper error handling and exception management
    - Input validation where necessary
    - Graceful degradation when things go wrong
    - Defensive programming practices

    ### 3. EFFICIENCY & PERFORMANCE (15 points)
    - Appropriate time and space complexity for the problem
    - Avoids unnecessary computations or redundant operations
    - Efficient use of data structures and algorithms
    - Scalability considerations

    ### 4. READABILITY & MAINTAINABILITY (20 points)
    - Clear and descriptive variable/function names
    - Proper code structure and organization
    - Appropriate comments and documentation
    - Follows PEP 8 style guidelines
    - Code is easy to understand and modify

    ### 5. PYTHONIC CODE & BEST PRACTICES (10 points)
    - Idiomatic use of Python features and libraries
    - Leverages built-in functions and standard library effectively
    - Follows Python conventions and design patterns
    - Avoids anti-patterns and code smells

    ## DETAILED ANALYSIS REQUIREMENTS

    ### BUILT-IN FUNCTIONS & IMPORTS ANALYSIS
    **Identify and evaluate:**
    - All Python built-ins used (len, sum, min, max, any, all, map, filter, zip, enumerate, range, sorted, list, dict, set, tuple, abs, print, open, input, etc.)
    - Usage frequency and appropriateness
    - Missed opportunities to use better built-ins
    - Security risks: eval, exec, open (write operations), subprocess, os.system, pickle (untrusted data), input (unvalidated)
    - Standard library imports vs third-party dependencies

    ### ALGORITHM & COMPLEXITY ANALYSIS
    - Summarize the algorithm approach in clear steps
    - Identify time complexity O(?) for dominant operations
    - Identify space complexity O(?) 
    - Performance bottlenecks and optimization opportunities

    ### SECURITY & SAFETY ASSESSMENT
    - Potential security vulnerabilities
    - Unsafe practices (eval, exec without safeguards)
    - Input validation and sanitization
    - File handling and resource management

    ### CODE QUALITY METRICS
    - PEP 8 compliance issues
    - Code duplication and DRY principle violations
    - Function/class design and single responsibility
    - Documentation quality (docstrings, comments)

    ## EVALUATION OUTPUT FORMAT

    Provide your evaluation in this structured format:

    **OVERALL SCORE: X/100**

    ### Executive Summary
    [Brief 2-3 sentence overview of code quality and main findings]

    ### Correctness & Functionality (X/40)
    **Algorithm Overview:** [Step-by-step breakdown of the logic]
    **Issues Found:** [List any bugs, errors, or logical problems]
    **Functionality Assessment:** [Does it work as intended?]

    ### Built-in Functions & Imports Analysis
    **Functions Identified:**
    - `function_name()` (used X times): [Purpose, appropriateness, risk level: none/low/medium/high]
    - `another_function()` (used X times): [Analysis]

    **Imports:**
    - Standard Library: [list modules]
    - Third-party: [list modules]
    - Missing Opportunities: [suggest better built-ins]

    ### Algorithm Efficiency & Complexity (X/15)
    **Time Complexity:** O(?)
    **Space Complexity:** O(?)
    **Performance Analysis:** [bottlenecks and optimization suggestions]
    **Scalability:** [how it performs with larger inputs]

    ### Robustness & Error Handling (X/15)
    **Edge Cases Handled:** [list what's covered]
    **Missing Edge Cases:** [what should be added]
    **Error Handling Quality:** [assessment of try/catch, validation]
    **Input Validation:** [presence and quality]

    ### Code Quality & Readability (X/20)
    **PEP 8 Compliance:** [style issues found]
    **Naming & Structure:** [variable/function naming quality]
    **Documentation:** [comments, docstrings assessment]
    **Code Organization:** [modularity, clarity]

    ### Pythonic Code & Best Practices (X/10)
    **Pythonic Patterns Used:** [good practices identified]
    **Anti-patterns Found:** [code smells, violations]
    **Library Usage:** [appropriate use of standard library]

    ### Security & Safety Assessment
    **Security Risks:** [potential vulnerabilities]
    **Unsafe Practices:** [dangerous code patterns]
    **Recommendations:** [security improvements]

    ### Test Case Suggestions
    1. **Normal Case:** Input: [example], Expected: [result]
    2. **Edge Case:** Input: [example], Expected: [result]
    3. **Error Case:** Input: [example], Expected: [behavior]

    ### Performance Optimization Suggestions
    - [Specific micro-optimizations]
    - [Algorithm improvements]
    - [Data structure recommendations]

    ## FINAL RECOMMENDATIONS

    ### Strengths
    - [What the code does well]
    - [Positive aspects to acknowledge]

    ### Critical Issues (Must Fix)
    - [High priority problems]
    - [Bugs or security concerns]

    ### Improvement Opportunities
    - [Medium priority enhancements]
    - [Best practice suggestions]

    ### Enhanced Code Example (if major improvements needed)
    ```python
    # Provide a refactored version demonstrating improvements
    # Focus on the most critical issues identified
    ```

    ## SPECIAL HANDLING INSTRUCTIONS

    **For Incomplete/Invalid Code:**
    - Set verdict to "fail" and explain issues clearly
    - Still provide analysis where possible
    - Focus on what can be improved or fixed

    **For Security Concerns:**
    - Always flag risky functions: eval, exec, pickle.load, subprocess, os.system
    - Highlight input validation gaps
    - Note file operation vulnerabilities

    **For Performance Issues:**
    - Always provide Big-O analysis
    - Identify specific bottlenecks
    - Suggest concrete optimization strategies

    IMPORTANT SCORING RULES:
    - Never exceed maximum points for any category (40, 15, 15, 20, 10)
    - Ensure all category scores sum to the overall score
    - Be consistent in scoring across similar code patterns
    - Justify significant point deductions with specific examples"""
    }

    user_message = {
        "role": "user",
        "content": f"""Please evaluate the following Python code according to your professional code evaluation framework:

    Question: {question}
    ```python
    {code}
    ```

    Provide a comprehensive analysis including:
    1. Overall score out of 100 with proper category breakdown
    2. Complete built-in functions analysis with risk assessment
    3. Algorithm complexity analysis (time/space)
    4. Security and safety evaluation
    5. Specific test case suggestions
    6. Performance optimization recommendations
    7. Enhanced code example if significant improvements are needed

    Be thorough, objective, and constructive in your evaluation. Focus on actionable feedback that helps improve code quality."""
    }

    payload = {
        "model": config.OLLAMA_MODEL,
        "messages": [system_message, user_message],
        "stream": False
    }

    try:
        response = requests.post(config.OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "No evaluation returned from the model.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"


def chat_with_ai(code: str, history: list[ChatMessage]) -> str:
    system_message = {
        "role": "system",
        "content": f"You are an expert code evaluator. The user has submitted the following Python code:\n\n```python\n{code}\n```\n\nYour previous evaluation and the user's follow-up questions are in the chat history. Please provide a helpful and relevant response to the user's last message."
    }

    messages = [system_message] + [msg.dict() for msg in history]

    payload = {
        "model": config.OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(config.OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "No evaluation returned from the model.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"


def evaluate_image(image_base64: str, prompt: str) -> str:
    user_message = {
        "role": "user",
        "content": prompt,
        "images": [image_base64]
    }

    payload = {
        "model": config.OLLAMA_MODEL,
        "messages": [user_message],
        "stream": False
    }

    try:
        response = requests.post(config.OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "No evaluation returned from the model.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"
