from llm_interface import LLM_Interface
from agent import Agent
from agent_system import AgentSystem
from memory_manager import MemoryManager  # Import MemoryManager
from web_search_tool import WebSearchTool  # Import WebSearchTool
from website_rag_tool import WebsiteRAGTool  # Import WebsiteRAGTool
from file_system_tool import FileSystemTool  # Import FileSystemTool
from local_rag_tool import LocalRAGTool  # Import LocalRAGTool
from website_expert_tool import WebsiteExpertTool  # Import WebsiteExpertTool
from fact_checker_agent import FactCheckerAgent  # Import the new agent

# --- LLM_Interface.py ---
# ... (The LLM_Interface class code from the previous response) ...

# --- Agent.py ---
# ... (The Agent class code from the previous response) ...

# --- AgentSystem.py ---
# ... (The AgentSystem class code from the previous response) ...

# --- memory_manager.py ---
# ... (The MemoryManager class code from the previous response) ...

if __name__ == "__main__":
    model_path = "locationformodel"  # Replace with actual path
    llm_interface = LLM_Interface(model_path)
    memory_manager = MemoryManager()  # Create MemoryManager instance
    agent_system = AgentSystem(llm_interface, memory_manager)

    # Create agents
    api_key = "YOUR_API_KEY"   # Replace with your Google Custom Search API Key
    search_engine_id = "YOUR_SEARCH_ENGINE_ID" # Replace with your Google Custom Search Engine ID
    web_searcher = Agent("Web Searcher", "Skilled at finding information on the web", ["web search"], api_key=api_key, search_engine_id=search_engine_id)
    document_expert = Agent("Document Expert", "Processes and extracts information from documents", ["document processing", "extract from website"], [LocalRAGTool(), WebsiteRAGTool()])  # Add WebsiteRAGTool 
    general_knowledger = Agent("General Knowledger", "Skilled at answering general knowledge questions", ["general knowledge"],  # Add tools for general knowledge
                                      # ...
                                      )
    # ... (Create more agents) ...
    # Create the fact-checking agent
    fact_checker = FactCheckerAgent()

    # Add the fact-checking agent to the agent system
    agent_system.add_agent(fact_checker)
    
    # Add agents to the agent system
    agent_system.add_agent(web_searcher)
    agent_system.add_agent(document_expert)
    agent_system.add_agent(general_knowledger)
    # ... (Add more agents) ...

    # Initialize context
    context = "The following is a conversation between a user and an AI."

    # User input
    user_input = "What are the main features of the iPhone 14 Pro?"  # Use a website-related question

    # Handle the task
    response = agent_system.handle_task(user_input)

    print("AI Response:", response)
    print("Updated Context:", agent_system.memory_manager.get_context())