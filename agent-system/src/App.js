// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [agents, setAgents] = useState([]);
  const [newAgent, setNewAgent] = useState({ name: '', description: '', skills: [] });

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await axios.get('urlforlocalhost');
        setAgents(response.data);
      } catch (error) {
        console.error("Error fetching agents:", error);
      }
    };
    fetchAgents();
  }, []);

  const handleInputChange = (e) => {
    setNewAgent({ ...newAgent, [e.target.name]: e.target.value });
  };

  const handleAddSkill = () => {
    setNewAgent({...newAgent, skills: [...newAgent.skills, ""]})
  }

  const handleSkillChange = (e, index) => {
    const newSkills = [...newAgent.skills];
    newSkills[index] = e.target.value;
    setNewAgent({ ...newAgent, skills: newSkills });
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('urlforlocalhost', newAgent);
      setNewAgent({ name: '', description: '', skills: [] });
      //Refetch agents
      const response = await axios.get('urlforlocalhost');
      setAgents(response.data);

    } catch (error) {
      console.error("Error adding agent:", error);
    }
  };

  return (
    <div>
      <h1>Teagardan Agents</h1>
      <ul>
        {agents.map((agent) => (
          <li key={agent.id}>
            {agent.name} - {agent.description} - {agent.skills}
          </li>
        ))}
      </ul>

      <h2>Add New Agent</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input type="text" name="name" value={newAgent.name} onChange={handleInputChange} required />
        </label>
        <br />
        <label>
          Description:
          <input type="text" name="description" value={newAgent.description} onChange={handleInputChange} />
        </label>
        <br />
        <label>Skills: </label> <br/>
        {newAgent.skills.map((skill,index) => (
          <div key={index}>
            <input type="text" name={`skills-${index}`} value={skill} onChange={(e)=>handleSkillChange(e, index)}/>
          </div>
        ))}
        <button onClick={handleAddSkill}>Add Skill</button>
        <br />
        <button type="submit">Add Agent</button>
      </form>
    </div>
  );
}

export default App;