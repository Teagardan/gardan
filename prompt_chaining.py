import os
from transformers import pipeline, AutoModelForSequenceClassification
from llama_cpp import Llama

class PromptChain:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None  # Initialize model to None
        self.chain = [] 

    def load_model(self):
        # Load the model dynamically
        if self.model_path:
            self.model = Llama.from_file(self.model_path)

    def add_prompt(self, prompt):
        self.chain.append(prompt)

    def run(self, input_text):
        response = input_text
        if self.model:
            for prompt in self.chain:
                llm_response = self.model.generate(prompt, n_predict=50)
                response += " " + llm_response
        else:
            response = "Model not loaded"
        return response