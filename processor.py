import random
from typing import List, Dict, Any, Tuple

def parse_answers(answer_string: str) -> List[int]:
    """
    Convert an answer string (e.g., '1 1 0 0') to a list of integers.

    Parameters
    ----------
    answer_string : str
        The answer string containing integers separated by spaces.

    Returns
    -------
    List[int]
        A list of integers representing correct (1) or incorrect (0) answers.
    """
    return [int(x) for x in answer_string.strip().split()]

def check_answer(user_answers: List[bool], correct_answers: List[int]) -> bool:
    """
    Check if the user's answers match the correct answers.

    Parameters
    ----------
    user_answers : List[bool]
        User's selected answers as booleans.
    correct_answers : List[int]
        The correct answers as integers (1 for correct, 0 for incorrect).

    Returns
    -------
    bool
        True if all user answers match the correct answers, False otherwise.
    """
    user_ints = [1 if x else 0 for x in user_answers]
    return user_ints == correct_answers[:len(user_ints)]

def get_question_type(question: Dict[str, Any]) -> Tuple[str, int]:
    """
    Determine the question type ('single' or 'multiple') and 
    the number of correct answers required.

    Parameters
    ----------
    question : Dict[str, Any]
        A dictionary representing a question.

    Returns
    -------
    Tuple[str, int]
        A tuple of (question_type, num_correct_answers).
    """
    correct_answers = parse_answers(question['Answers'][0])
    num_correct = sum(correct_answers)
    return ('single' if num_correct == 1 else 'multiple', num_correct)

def get_shuffled_options(question: Dict[str, Any]) -> Tuple[List[str], List[int]]:
    """
    Get shuffled answer options and their corresponding correct answers.

    Parameters
    ----------
    question : Dict[str, Any]
        A dictionary representing a question, including its 'Answers' and 'Q_1'...'Q_6' fields.

    Returns
    -------
    Tuple[List[str], List[int]]
        A tuple (shuffled_options, new_correct_answers) where:
        - shuffled_options is a list of option strings.
        - new_correct_answers is a list of ints (1 or 0) aligned with shuffled_options.
    """
    options = []
    correct_answers = parse_answers(question['Answers'][0])
    
    # Collect non-empty options and their corresponding correct answers
    for i in range(1, 7):  # Q_1 through Q_6
        option = question.get(f'Q_{i}', '').strip()
        if option:
            answer = correct_answers[i-1] if i-1 < len(correct_answers) else 0
            options.append((option, answer))
    
    random.shuffle(options)
    
    shuffled_options = [opt for opt, _ in options]
    new_correct_answers = [ans for _, ans in options]
    
    return shuffled_options, new_correct_answers

def validate_question_format(question: Dict) -> tuple[bool, str]:
    """Validate if the question has the required fields"""
    required_fields = ['Question', 'Answers']
    
    for field in required_fields:
        if field not in question:
            return False, f"Missing required field: {field}"
            
    if not isinstance(question['Answers'], (list, str)):
        return False, "Invalid 'Answers' format: must be a list or string"
        
    return True, ""

def validate_questions(questions: List[Dict]) -> tuple[bool, str]:
    """Validate all questions in the deck"""
    if not questions:
        return False, "No questions found in the deck"
        
    for i, question in enumerate(questions):
        is_valid, error_msg = validate_question_format(question)
        if not is_valid:
            return False, f"Question {i+1}: {error_msg}"
            
    return True, ""