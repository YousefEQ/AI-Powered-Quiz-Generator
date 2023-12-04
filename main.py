# main.py
import streamlit as st
from quiz_generator import QuizGenerator
from utils import parse_question

def main():
    st.title("Dynamic MCQ Quiz Application")

    # Initialize QuizGenerator with your OpenAI API key
    OPENAI_API_KEY = 'API key'  
    quiz_gen = QuizGenerator(OPENAI_API_KEY)

    if 'questions' not in st.session_state:
        initialize_state()

    topic = st.text_input("Enter the quiz topic:")
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=10, value=5)

    # Start Quiz button section
    if 'start_button' not in st.session_state:
        st.session_state.start_button = True

    if st.session_state.start_button:
        if st.button("Start Quiz") and topic:
            start_new_quiz(topic, num_questions, quiz_gen)
            st.session_state.start_button = False  # Disable the 'Start Quiz' button
            st.experimental_rerun()  # Rerun the app to reset the state

    display_questions()

    # Submit Quiz button section
    submit_button = st.empty()
    if st.session_state.quiz_started and not st.session_state.quiz_submitted and all_answered():
        if submit_button.button("Submit Quiz"):
            st.session_state.quiz_submitted = True
            submit_button.empty()  # Remove the 'Submit Quiz' button after it's pressed
            st.session_state.score = mark_answers(num_questions)
            st.session_state.display_results = True
            st.experimental_rerun()  # Rerun the app to update the state

    # Display results after submission
    if st.session_state.display_results:
        display_results(num_questions)

def initialize_state():
    st.session_state.questions = []
    st.session_state.user_answers = {}
    st.session_state.correct_answers = []
    st.session_state.display_results = False
    st.session_state.quiz_started = False
    st.session_state.quiz_submitted = False
    st.session_state.start_button = True

def start_new_quiz(topic, num_questions, quiz_gen):
    st.session_state.questions = [quiz_gen.generate_question(topic) for _ in range(num_questions)]
    st.session_state.user_answers = {i: None for i in range(1, num_questions + 1)}
    st.session_state.correct_answers = [parse_question(q)[2] for q in st.session_state.questions]
    st.session_state.quiz_started = True

def display_questions():
    if st.session_state.quiz_started:
        for i, q_text in enumerate(st.session_state.questions, start=1):
            question, options, _ = parse_question(q_text)
            st.markdown(f"**Question {i}: {question}**")
            option_labels = [""] + [f"{label}) {text}" for label, text in options.items()]
            disabled = st.session_state.quiz_submitted
            chosen_option = st.radio("", option_labels, index=0, key=f"Q_{i}", disabled=disabled)
            if chosen_option and not disabled:
                st.session_state.user_answers[i] = chosen_option.split(')')[0]

def mark_answers(num_questions):
    score = 0
    for i in range(1, num_questions + 1):
        question_text = st.session_state.questions[i-1]
        _, _, correct_answer_key = parse_question(question_text)
        user_answer = st.session_state.user_answers.get(i, "")
        score += user_answer == correct_answer_key.upper()  # Ensure correct answer key is upper case
    return score

def display_results(num_questions):
    st.write(f"Your score: {st.session_state.score}/{num_questions}")
    for i in range(1, num_questions + 1):
        question_text = st.session_state.questions[i-1]
        _, _, correct_answer_key = parse_question(question_text)
        user_answer = st.session_state.user_answers.get(i, "")
        is_correct = user_answer == correct_answer_key.upper()  # Ensure correct answer key is upper case
        color = "green" if is_correct else "red"
        st.markdown(f"**Question {i}: <span style='color: {color};'>{'Correct' if is_correct else 'Incorrect'}</span>**", unsafe_allow_html=True)
        st.write(f"Your answer: {user_answer}")
        if not is_correct:
            st.write(f"Correct Answer: {correct_answer_key.upper()}")

def all_answered():
    return all(answer is not None for answer in st.session_state.user_answers.values())

if __name__ == "__main__":
    main()
