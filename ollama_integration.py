import subprocess

class LLM_Interface:
    def __init__(self, model_name="llama3.2:1b-text-q8_0"):
        self.model_name = model_name

    def generate_text(self, prompt):
        """
        Generates text using the Ollama model based on the given prompt.
        """
        try:
            # Run the ollama run command to generate text with the input prompt
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Check if there were errors
            if result.stderr:
                print(f"Error: {result.stderr}")
                return None

            print(f"Response: {result.stdout.strip()}")
            return result.stdout.strip()

        except Exception as e:
            print(f"Exception: {str(e)}")
            return None

# Usage
llm_interface = LLM_Interface()
prompt = "What is the capital of France?"
response = llm_interface.generate_text(prompt)

if response:
    print(f"Generated Response: {response}")
