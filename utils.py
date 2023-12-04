# utils.py
import re

def parse_question(question_text):
    """Parse the given question text to extract the question, options, and correct answer."""
    parts = question_text.split("Correct answer:")
    question_and_options = parts[0].strip()
    question, options_text = extract_question_and_options(question_and_options)
    options = extract_options(options_text)
    correct_answer = parts[1].strip().split()[0].replace(")", "").strip() if len(parts) > 1 else None
    return question, options, correct_answer

def extract_question_and_options(text):
    """Extract the question and its options from the given text."""
    if '\n' in text:
        split_text = text.split('\n', 1)
        return split_text[0].strip(), split_text[1].strip()
    else:
        split_text = re.split(r'\s+[A-Da-d]\)', text, maxsplit=1)
        return split_text[0].strip(), split_text[1].strip() if len(split_text) > 1 else ''

def extract_options(text):
    """Extract the options from the given text and return them as a dictionary."""
    options = {}
    pattern = r'([A-Da-d])\)\s*(.*?)\s*(?=[A-Da-d]\)|$)'
    for match in re.findall(pattern, text, re.DOTALL):
        options[match[0].upper()] = match[1].strip()
    return options
