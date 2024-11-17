const handleTaskSubmit = (taskDescription) => {
    const updatedAgents = [...agents]; // Create a copy of the agents array
  
    // Find the appropriate agent for the task (e.g., based on skills)
    const agentIndex = updatedAgents.findIndex(agent => agent.skills.includes('Web Search'));
  
    if (agentIndex !== -1) {
      updatedAgents[agentIndex].currentTask = taskDescription; // Assign the task
      setAgents(updatedAgents);
    } else {
      // Handle the case where no suitable agent is found
      alert('No agent with the required skills found.');
    }
  };