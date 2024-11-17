import os
import subprocess
from transformers import pipeline, AutoModelForSequenceClassification
from llama_cpp import Llama
from prompt_chaining import PromptChain  # Import PromptChain
import logging
logging.basicConfig(level=logging.WARNING)  # Suppress info-level messages

class LLM_Interface:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self.prompt_chain = None
        self.prompt_templates = {
            "question_answer": self.build_question_answer_prompt,
            "reasoning": self.build_reasoning_prompt,
        }
        if self.model_path:
            self.load_model()

    def load_model(self):
        if self.model_path:
            if self.model_path.endswith('.gguf'):
                self.model = Llama(model_path=self.model_path, verbose=0)  # Suppress loading messages
            else:
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.prompt_chain = PromptChain(self.model_path)

    def build_prompt(self, context, user_input, template_type="question_answer"):
        if template_type in self.prompt_templates:
            return self.prompt_templates[template_type](context, user_input)
        else:
            return f"{context}\nUser: {user_input}\nAI:"

    def build_question_answer_prompt(self, context, user_input):
        few_shot_examples = """
        Example 1:
        User: What is 2 + 2?
        AI: 2 + 2 equals 4.

        Example 2:
        User: What is the capital of France?
        AI: The capital of France is Paris.
        """
        return f"{context}\n{few_shot_examples}\nUser: {user_input}\nAI:"

    def build_reasoning_prompt(self, context, user_input):
        return f"{context}\nUser: {user_input}\nAI: To understand this, let's break it down: \n\n" \
            f"Step 1:  What are some key concepts related to {user_input}? (Most important step) \n\n" \
            f"Step 2:  How do these concepts relate to each other? \n\n" \
            f"Step 3:  What are some possible interpretations of {user_input} based on these concepts? \n\n" \
            f"Final Answer: "

    def generate_text(self, prompt):
        if self.model_path.endswith('.gguf'):
            command = [
                "ollama", "run", "llama3.2:3b-instruct-q8_0",
                prompt
            ]
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                print(f"Error running the model: {e}")
                return ""
        else:
            return pipeline('text-generation', model=self.model)(prompt, max_length=50)[0]['generated_text'].strip()

    def parse_response(self, response):
        return response.strip()

    def manage_context(self, context, new_message, max_tokens=2048):
        updated_context = f"{context}\n{new_message}"
        token_count = len(updated_context.split())
        if token_count > max_tokens:
            context_chunks = updated_context.split("\n")
            updated_context = "\n".join(context_chunks[-max_tokens:])
        return updated_context

    def summarize_response(self, response, max_length=100):
        summarizer = pipeline('summarization')
        return summarizer(response, max_length=max_length, min_length=50)[0]['summary_text'].strip()

    def ask(self, question, context=None):
        if self.prompt_chain:
            response = self.prompt_chain.run(question)
            concise_response = self.summarize_response(response)
            return concise_response
        else:
            return "Model not loaded"