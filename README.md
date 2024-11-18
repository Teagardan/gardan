## Hi there 👋

<!--
**teagardan/teagardan** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

## Getting Started

This guide helps you set up and run the Teagardan project.

**Prerequisites:**

*   Git
*   Python 3.11 (or later)  with the following packages: `flask`, `sqlite3`, `llama-cpp`, `requests`, `sentence-transformers` (see `requirements.txt` for a complete list).
*   Node.js and npm (for the frontend)
*   An LLM model (e.g., a GGML model in `.gguf` format) for local use.  Place this model in a directory specified in `api.py`.  You may have to make a directory for your model files.
*   Ollama (if you want to use ollama models)


**Steps:**

1.  **Clone the Repository:** `git clone <your_repo_url>`

2.  **Create the Database:** Create a SQLite database file named `agent_data.db` in the `masterplan` directory.  (The database is created automatically if it does not exist, when the server starts, but you might want to pre-create one if needed.)

3.  **Install Python Dependencies:** Navigate to the `masterplan` directory and run: `pip install -r requirements.txt` (This assumes you have a `requirements.txt` file listing all required Python packages.)

4.  **Install Frontend Dependencies:** Navigate to the `masterplan/agent-system` directory and run: `npm install`

5.  **Configure the LLM:** Update the `model_path` variable in `masterplan/api.py` to point to your local LLM model file. For example:  `model_path = "/path/to/your/llama-model.gguf"`

6.  **Run the Flask Server:** Navigate to the `masterplan` directory and run: `python api.py` (This starts the Flask web server on the specified port. Check for the `port` variable in `api.py`)

7.  **Start the React Development Server (Optional, for web UI):** If you are using the React application, navigate to the `masterplan/agent-system` directory and run `npm start`. This will start a development server and open the application in your browser (usually on port 8080).


8.  **Access the UI:** Open your web browser and navigate to the URL specified by your Flask or React development server.  The URL will usually be `localhost` for the React UI and  `localhost' for API access.

For more advanced setup, usage instructions, and details on contributing, please refer to the documentation.
