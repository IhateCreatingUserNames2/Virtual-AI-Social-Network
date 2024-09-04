import requests
import sqlite3
import os
from models.ml_models.agent_llm import AgentLLM  # Import the AgentLLM class

# DeepAI API key
api_key = '7c5f0825-9c84-4ed0-8721-8ecd6abf4e63'

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'

# Path to save the profile pictures
img_path = 'E:/ProjetosPython/NEWAI/data/img/'

# Ensure the image directory exists
os.makedirs(img_path, exist_ok=True)

# Initialize the AgentLLM with the llama3 model through Ollama
agent_llm = AgentLLM("llama3")


def generate_profile_picture(description):
    url = "https://api.deepai.org/api/text2img"
    response = requests.post(
        url,
        data={
            'text': description,
        },
        headers={'api-key': api_key}
    )
    return response.json()


def save_profile_picture(agent_name, image_url):
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        image_filename = f"{agent_name}.jpg"
        image_path = os.path.join(img_path, image_filename)
        with open(image_path, 'wb') as f:
            f.write(image_response.content)
        return image_filename
    else:
        print(f"Failed to download image for {agent_name}")
        return None


def generate_agent_self_description(agent_profile, agent_name):
    """
    Generate a text description of the agent's appearance based on their profile and characteristics.
    This function interacts with the agent's model to produce a prompt.
    """
    description = f"Imagine if you are a person with the characteristics: {agent_profile}. Return only a Prompt for Image Creation on DeepAI. Example: "

    # Sending the description to the agent's LLM (llama3) to generate a prompt
    generated_prompt = agent_llm.generate_response(description, personality=agent_name)

    return generated_prompt


def trigger_agent_profile_pictures():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all agents
    cursor.execute("SELECT id, name, profile FROM agents")
    agents = cursor.fetchall()

    for agent in agents:
        agent_id, agent_name, agent_profile = agent
        print(f"Generating profile picture for {agent_name}...")

        # Generate the agent's self-description
        description = generate_agent_self_description(agent_profile, agent_name)
        print(f"Agent {agent_name} self-description: {description}")

        # Generate profile picture
        response = generate_profile_picture(description)
        if 'output_url' in response:
            # Save the profile picture locally
            image_filename = save_profile_picture(agent_name, response['output_url'])

            if image_filename:
                # Update the agent's profile_picture field in the database
                cursor.execute(
                    "UPDATE agents SET profile_picture = ? WHERE id = ?",
                    (image_filename, agent_id)
                )
                conn.commit()
                print(f"Profile picture saved for {agent_name}")
        else:
            print(f"Failed to generate image for {agent_name}: {response}")

    # Close the connection
    conn.close()


if __name__ == "__main__":
    trigger_agent_profile_pictures()
