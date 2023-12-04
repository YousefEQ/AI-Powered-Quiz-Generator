# quiz_generator.py
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

class QuizGenerator:
    """A class to generate unique quiz questions using OpenAI's ChatGPT."""

    def __init__(self, openai_api_key, model_name="gpt-3.5-turbo"):
        """Initialize the ChatOpenAI model with the given API key and model name."""
        self.chat_model = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key)
        self.generated_questions = set()

    def generate_question(self, topic):
        """Generate a unique quiz question on the given topic."""
        retry_limit = 5
        for _ in range(retry_limit):
            prompt = f"Create a unique multiple choice question about {topic}. make sure you don't ask a question more than once. Include 4 answer choices and indicate the correct one."
            response = self.chat_model([HumanMessage(content=prompt)])
            question = response.content.strip() if response.content else None

            if question and question not in self.generated_questions:
                self.generated_questions.add(question)
                return question
        return "Unable to generate a unique question after several attempts."

