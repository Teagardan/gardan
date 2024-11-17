import re

class AgentSystem:
    def __init__(self, llm_interface, memory_manager):
        self.llm_interface = llm_interface
        self.memory_manager = memory_manager
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def get_agent(self, agent_name):
        for agent in self.agents:
            if agent.name == agent_name:
                return agent
        return None

    def assign_task(self, task):
        # Logic for task assignment (e.g., round-robin, based on skills)
        if "fact-check" in task.lower():
            agent = self.get_agent("Fact Checker")
            if agent:
                response = agent.handle_task(task)
                return agent, response
        elif "extract from website" in task.lower():
            agent = self.get_agent("Document Expert")
            if agent:
                response = agent.handle_task(task)
                return agent, response
            
        decomposed_tasks = self.decompose_task(task)  # Attempt to decompose the task
        if decomposed_tasks:
            for subtask in decomposed_tasks:
                agent, subtask_response = self.assign_task(subtask)  # Recursively assign subtasks
                print(f"Subtask: '{subtask}' handled by agent: '{agent.name}'")
                print(f"Subtask Response: '{subtask_response}'")
            return None, None  # No direct response, subtasks are handled recursively
        else:
            # If task can't be decomposed, assign it as usual
            agent = self.agents[0]
            response = agent.handle_task(task)
            return agent, response

    def decompose_task(self, task):
        subtasks = self.llm_interface.generate_text(f"Break down the task '{task}' into smaller subtasks:").split("\n")
        return [subtask.strip() for subtask in subtasks if subtask.strip()]  # Return list of subtasks
    
        # You'll likely want to replace this with more sophisticated logic
        pattern = r"([A-Z][a-z]+)\s+(.+)"  # Match a verb followed by the task description
        match = re.match(pattern, task)
        if match:
            verb, description = match.groups()
            subtasks = self.llm_interface.generate_text(f"Break down the task '{description}' into smaller subtasks:").split("\n")
            return [f"{verb} {subtask.strip()}" for subtask in subtasks if subtask.strip()]
        return None  # No decomposition possible

    def handle_task(self, task):
        # Logic for task handling (e.g., pass to the assigned agent)
        agent, response = self.assign_task(task)  # Assign task and get response
        return response  # Return response to the task