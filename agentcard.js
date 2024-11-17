import React from 'react';

const AgentCard = ({ agent }) => {
  return (
    <div className="agent-card">
      <h2>{agent.name}</h2>
      <p>Type: {agent.type}</p>
      <ul>
        {agent.skills.map(skill => <li key={skill}>{skill}</li>)}
      </ul>
      <p>Current Task: {agent.currentTask || 'Idle'}</p>
      {/* ... (Optional UI elements) ... */}
    </div>
  );
};

export default AgentCard;