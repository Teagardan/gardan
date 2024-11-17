fetch('urlforlocal')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('Fetched data:', data);
    const agentList = document.getElementById('agent-list');
    if (agentList) {
      let html = '';
      if(data.length === 0){
        html = "<p>No agents found.</p>";
      } else {
        data.forEach(agent => {
          html += `<div><h3>${agent.name}</h3><p>Description: ${agent.description}</p><p>Skills: ${agent.skills.join(', ')}</p></div>`;
        });
      }
      agentList.innerHTML = html;
    } else {
      console.error("agent-list div not found!");
    }
  })
  .catch(error => {
    console.error('Error fetching agents:', error);
    const agentList = document.getElementById('agent-list');
    if (agentList) {
      agentList.innerHTML = `<p>Error: ${error.message}</p>`;
    }
  });