import subprocess
from llm_interface import LLM_Interface  # Import the LLM_Interface
from web_search_tool import WebSearchTool  # Import the WebSearchTool
from website_rag_tool import WebsiteRAGTool  # Import the WebsiteRAGTool
from file_system_tool import FileSystemTool  # Import the FileSystemTool
from local_rag_tool import LocalRAGTool  # Import the LocalRAGTool
from website_expert_tool import WebsiteExpertTool  # Import the WebsiteExpertTool
from memory_manager import MemoryManager  # Import MemoryManager

class Agent:
    def __init__(self, name, description, skills, tools=None, llm_interface=None, memory_manager=None, api_key=None, search_engine_id=None):
        self.name = name
        self.description = description
        self.skills = skills  # Dictionary of skills and associated LLM models
        self.tools = tools or []
        self.llm_interface = llm_interface  # Keep the llm_interface for general use
        self.memory_manager = memory_manager or MemoryManager()  # Default Memory Manager
        self.context = ""  # Initialize context
        if "web search" in self.skills:
            self.tools.append(WebSearchTool(api_key, search_engine_id))  # Pass the API key and search engine ID
        if "extract from website" in self.skills:
            self.tools.append(WebsiteRAGTool())  # Add WebsiteRAGTool if the agent has "extract from website" skill
        if "access files" in self.skills:
            self.tools.append(FileSystemTool())  # Add FileSystemTool if the agent has "access files" skill
        if "extract from document" in self.skills:
            self.tools.append(LocalRAGTool())  # Add LocalRAGTool if the agent has "extract from document" skill
        if "access website experts" in self.skills:
            self.tools.append(WebsiteExpertTool())  # Add WebsiteExpertTool if the agent has "access website experts" skill
        if "general knowledge" in self.skills:
            self.skills.append("philosophical reasoning")  # Add this line
            self.llm_interface = llm_interface or LLM_Interface(model_path="locationformodel")  # Default LLM_Interface
            self.memory_manager = memory_manager or MemoryManager()  # Default Memory Manager
            self.context = ""  # Initialize context

    def handle_task(self, task):
        # 1. Assess Task Suitability
        if not self.is_suitable_task(task):
            return f"I'm sorry, I'm not equipped to handle a task like this. My skills are: {', '.join(self.skills)}."

        # 2. Use Tools (if needed)
        if self.requires_tools(task):
            response = self.use_tools(task)
            return response

        # 3. Construct Prompt
        # Determine the relevant skill for the task 
        relevant_skill = self.determine_relevant_skill(task)
        if relevant_skill:
            skill_model_path = self.skills.get(relevant_skill)
            if skill_model_path:
                skill_llm = LLM_Interface(model_path=skill_model_path)
                skill_llm.load_model()
                prompt = skill_llm.build_prompt(self.context, task)
                response = skill_llm.generate_text(prompt)
                response = skill_llm.parse_response(response)
            else:
                response = f"I don't have a suitable model for that skill: {relevant_skill}"
        else:
            prompt = self.llm_interface.build_prompt(self.context, task)
            response = self.llm_interface.generate_text(prompt)
            response = self.llm_interface.parse_response(response)

        # 4. Update Context
        self.update_context(task, response)

        return response

    def is_suitable_task(self, task):
        print(f"Checking task suitability for task: '{task}' with skills: {self.skills}")
        
        # Mapping specific skills to a set of keywords
        skill_keywords = {
            "web search": ["search", "find", "lookup", "information", "features", "details"]
            # Add more mappings if needed
        }

        # Check if any mapped keywords for each skill are in the task
        for skill in self.skills:
            keywords = skill_keywords.get(skill, [])
            for keyword in keywords:
                if keyword in task.lower():
                    print(f"Skill '{skill}' matched with keyword '{keyword}' in task '{task}'")
                    return True

        print("No suitable skills found for task.")
        return False


    def requires_tools(self, task):
        # Simple implementation: Check if any tool is mentioned in the task
        for tool in self.tools:
            tool_name = type(tool).__name__.lower()  # Get the tool's class name in lowercase
            if tool_name in task.lower():
                return True
        return False

    def use_tools(self, task):
        for tool in self.tools:
            if isinstance(tool, WebSearchTool):
                search_results = tool.search(task)  # Call search method
                return "Search results: " + search_results
            elif isinstance(tool, WebsiteRAGTool):
                # Extract a URL from the task, or use a predefined URL
                url = "https://www.apple.com/iphone/compare"  # Example: Predefined URL for iPhone 14 Pro features
                extracted_info = tool.extract_information(url, task)  # Pass the URL 
                return "Extracted Information: " + extracted_info  # Update this line to return the extracted_info
            elif isinstance(tool, FileSystemTool):
                if "read" in task.lower():
                    file_content = tool.read_file("data.txt")
                    return file_content
                elif "write" in task.lower():
                    result = tool.write_file("output.txt", "This is some content to write.")
                    return result
            elif isinstance(tool, LocalRAGTool):
                extracted_info = tool.extract_information("data.txt", task)  # Call extract_information method
                return "Extracted Information: " + extracted_info
            elif isinstance(tool, WebsiteExpertTool):
                if "expert on" in task.lower():
                    website = task.split("expert on")[1].strip()  # Extract the website from the task
                    expert_info = tool.get_expert_information(website, task)  # Call get_expert_information method
                    return "Expert Information: " + expert_info
        return "Tool results"

    def current_context(self):
        return self.context  # Return the current context

    def update_context(self, task, response):
        self.context += f"\nUser: {task}\nAI: {response}"  # Append to context
        self.memory_manager.update_context(task, response)  # Store in Memory Manager

    # NEW: Function to determine relevant skill for the task
    def determine_relevant_skill(self, task):
        # Define keywords for each skill
        skill_keywords = {
            "web search": ["search", "find", "lookup", "query", "internet", "google", "information", "research"],
            "extract from website": ["website", "webpage", "content", "extract", "scrape"],
            "access files": ["file", "read", "write", "access", "manage"],
            "extract from document": ["document", "extract", "text", "data", "parse"],
            "access website experts": ["expert", "knowledge", "specialist", "consult"],
            "philosophical reasoning": ["meaning", "life", "existence", "universe", "philosophy"]
        }

        best_match_count = 0
        best_match_skill = None

        # Normalize task to lowercase for case-insensitive matching
        task_lower = task.lower()

        print(f"Task being processed: {task_lower}")  # Debugging print to verify the task

        # Check if the task includes any of the keywords
        for skill, keywords in skill_keywords.items():
            match_count = sum(1 for keyword in keywords if keyword in task_lower)
            print(f"Skill: {skill}, Match Count: {match_count}")  # Debugging print to check matches

            # Select skill with the highest match count
            if match_count > best_match_count:
                best_match_count = match_count
                best_match_skill = skill
            elif match_count == best_match_count and match_count > 0:
                # Handle tie with a priority order for cases with equal matches
                priority_order = ["access website experts", "web search", "extract from website", "extract from document", "access files", "philosophical reasoning"]
                if priority_order.index(skill) < priority_order.index(best_match_skill):
                    best_match_skill = skill

        print(f"Best Match Skill: {best_match_skill}")  # Debugging print to verify final match
        return best_match_skill if best_match_count > 0 else None

    def generate_text(self, prompt):
        if self.model_path.endswith('.gguf'):
            # Use Ollama for .gguf models
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
            # Use Hugging Face Transformers pipeline for other models
            return pipeline('text-generation', model=self.model)(prompt, max_length=50)[0]['generated_text'].strip()