// frontend/src/agentSystem.js
import axios from 'axios';

const agentSystem = {
  async loadAgents() {
    try {
      const response = await axios.get('urlforlocalhost'); //Correct URL and port
      return response.data;
    } catch (error) {
      console.error("Error loading agents:", error);
      return []; // Return an empty array if there's an error
    }
  },
  async addAgent(newAgent){
    try{
      const response = await axios.post('urlforlocalhost', newAgent);
      return response;
    } catch (error){
      console.error("Error adding agent:", error);
      return [];
    }
  }
};

export default agentSystem;