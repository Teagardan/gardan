# memory_manager.py
class MemoryManager:
    def __init__(self, max_context_size=1024): #Added max size
        self.context = []
        self.max_context_size = max_context_size

    def get_context(self):
        return "\n".join(self.context)

    def update_context(self, task, response):
        message = f"\nUser: {task}\nAI: {response}"
        self.context.append(message)
        if len(self.context) > self.max_context_size:
            self.context.pop(0) #Remove oldest message