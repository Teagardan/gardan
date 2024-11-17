from flask import Flask, request, jsonify
from agent_system import AgentSystem
from llm_interface import LLM_Interface
from memory_manager import MemoryManager
from agent import Agent
import sqlite3
import json
import os

app = Flask(__name__)
model_path = "locationformodel"  # <--- ABSOLUTELY CRITICAL:  CORRECT PATH TO YOUR MODEL!
llm_interface = LLM_Interface(model_path)
memory_manager = MemoryManager()
agent_system = AgentSystem(llm_interface, memory_manager)

# Example agents (replace with your actual agent creation)  Improve this section later.
qa_agent = Agent("QA Agent", "Answers questions.", ["question_answering"], llm_interface)
agent_system.add_agent(qa_agent)

# Make the database path relative to the api.py file
db_path = os.path.join(os.path.dirname(__file__), 'agent_data.db')

def create_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            skills TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_db()


@app.route('/agents', methods=['GET'])
def get_agents():
    print("get_agents function entered")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agents")
        agents = cursor.fetchall()
        conn.close()
        print(f"get_agents: Agents fetched from database: {agents}")

        if agents:
            agent_dicts = []
            for row in agents:
                try:
                    skills = json.loads(row[3])  # Try to load skills as JSON
                    agent_dicts.append({'id': row[0], 'name': row[1], 'description': row[2], 'skills': skills})
                except json.JSONDecodeError:
                    print(f"get_agents: Invalid JSON in skills column for agent ID {row[0]}: {row[3]}")
                    #Handle the error appropriately, e.g., log it, skip the agent, or return a partial response.
                    continue #Skip agents with invalid JSON for now.
            print(f"get_agents: Returning JSON: {agent_dicts}")
            return jsonify(agent_dicts), 200
        else:
            print("get_agents: No agents found.")
            return jsonify([]), 200

    except sqlite3.Error as e:
        print(f"get_agents: SQLITE error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        print(f"get_agents: Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/agents', methods=['POST'])
def add_agent():
    print("add_agent function entered")
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        skills = json.dumps(data.get('skills', []))

        if not name:
            return jsonify({'error': 'Agent name is required'}), 400

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO agents (name, description, skills) VALUES (?, ?, ?)", (name, description, skills))
        conn.commit()
        new_agent_id = cursor.lastrowid
        conn.close()
        print(f"add_agent: Agent '{name}' added successfully.")
        return jsonify({'message': 'Agent added successfully', 'id': new_agent_id}), 201
    except sqlite3.IntegrityError as e:  #More specific error handling
        print(f"add_agent: IntegrityError: {e}") #Show error message
        return jsonify({'error': 'Agent with that name already exists'}), 409
    except sqlite3.Error as e: #More specific error handling
        print(f"add_agent: SQLITE error: {e}") #Show error message
        return jsonify({"error": f"Database error: {e}"}), 500  #Return more details
    except json.JSONDecodeError as e: # Catch JSON decoding errors
        print(f"add_agent: JSONDecodeError: {e}") #Show error message
        return jsonify({"error": f"Invalid JSON data: {e}"}), 400 #Return more details
    except Exception as e:  #Catch other, unexpected errors.
        print(f"add_agent: Unexpected error: {e}") #Show error message
        return jsonify({"error": f"Internal server error: {e}"}), 500 #Return more details

from flask import Flask, request, jsonify
# ... other imports ...

@app.route('/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    print(f"delete_agent function called with agent_id: {agent_id}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agents WHERE id = ?", (agent_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        if rows_affected > 0:
            print(f"delete_agent: Agent with ID {agent_id} deleted successfully.")
            return jsonify({"message": "Agent deleted successfully"}), 200
        else:
            print(f"delete_agent: Agent with ID {agent_id} not found.")
            return jsonify({"error": "Agent not found"}), 404
    except sqlite3.Error as e:
        print(f"delete_agent: SQLITE error: {e}")
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        print(f"delete_agent: Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Flask app starting...")
    app.run(debug=True, port=5001)