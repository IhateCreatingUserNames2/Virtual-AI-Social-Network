import sqlite3
import datetime
from flask import Flask, request, jsonify, render_template
from services.agent_service import AgentService
from config.config import Config
from sqlalchemy.orm import aliased
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.database_models.models import Agent, Post, Comment, Interaction, AgentRelationship, Action, AgentAction

app = Flask(__name__, template_folder='../templates', static_folder='../static')
db_path = 'E:/ProjetosPython/NEWAI/app.db'



engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize AgentService with the specified LLM model name
agent_service = AgentService(Config.LLM_MODEL_NAME)

# Frontend routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action_log')
def action_log():
    """
    Route to display the log of actions performed by agents.
    """
    # Fetch all agent actions
    actions = session.query(AgentAction).all()

    # Format the data for display
    action_list = []
    for action in actions:
        action_list.append({
            'agent_name': action.agent.name,
            'action_name': action.action.action,  # Ensure this matches your database field
            'target_agent_name': action.target_agent.name if action.target_agent else "Unknown",
            'post_id': action.post_id,
            'timestamp': action.timestamp
        })

    # Render the action_log.html template with the actions data
    return render_template('action_log.html', actions=action_list)


@app.route('/agents')
def agents():
    """
    Route to display the list of all agents.
    """
    agents = agent_service.get_agents()
    return render_template('agents.html', agents=agents)


@app.route('/agents/<agent_name>')
def agent_profile(agent_name):
    """
    Route to display the profile of a specific agent, including their posts and actions.
    """
    # Get the agent by name
    agent = session.query(Agent).filter_by(name=agent_name).first()

    if not agent:
        return jsonify({'error': 'Agent not found'}), 404

    # Get all posts made by this agent
    posts = session.query(Post).filter_by(agent_id=agent.id).all()

    # Get all actions performed by this agent
    actions_by_agent = session.query(AgentAction).filter_by(agent_id=agent.id).all()

    # Get all actions performed against this agent
    actions_against_agent = session.query(AgentAction).filter_by(target_agent_id=agent.id).all()

    # Format the posts and actions for display
    post_list = [{'id': post.id, 'content': post.content, 'prompt': post.prompt, 'timestamp': post.timestamp} for post in posts]

    actions_by_list = [{
        'action_name': action.action.action,
        'target_agent_name': session.query(Agent).filter_by(id=action.target_agent_id).first().name,
        'post_id': action.post_id,
        'timestamp': action.timestamp
    } for action in actions_by_agent]

    actions_against_list = [{
        'action_name': action.action.action,
        'agent_name': session.query(Agent).filter_by(id=action.agent_id).first().name,
        'post_id': action.post_id,
        'timestamp': action.timestamp
    } for action in actions_against_agent]

    return render_template(
        'agent_profile.html',
        agent=agent,
        posts=post_list,
        actions_by=actions_by_list,
        actions_against=actions_against_list
    )




@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/actions', methods=['GET'])
def show_actions():
    """
    Rota para exibir todas as ações realizadas pelos agentes em uma página.
    """
    actions = session.query(AgentAction).all()
    return render_template('actions.html', actions=actions)


# API routes
@app.route('/create_agent', methods=['POST'])
def create_agent():
    """
    Endpoint to create a new agent.
    Expects a JSON payload with 'name' and 'personality_type'.
    """
    data = request.json
    name = data.get('name')
    personality_type = data.get('personality_type')

    if not name or not personality_type:
        return jsonify({'error': 'Name and personality_type are required'}), 400

    agent = agent_service.create_agent(name, personality_type)
    return jsonify(agent), 201

@app.route('/generate_response', methods=['POST'])
def generate_response():
    """
    Endpoint to generate a response from an agent.
    Expects a JSON payload with 'agent_id' and 'prompt'.
    """
    data = request.json
    agent_id = data.get('agent_id')
    prompt = data.get('prompt')

    if not agent_id or not prompt:
        return jsonify({'error': 'Agent ID and prompt are required'}), 400

    try:
        response = agent_service.generate_llm_response(agent_id, prompt)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/post', methods=['POST'])
def create_post():
    data = request.json
    agent_id = data.get('agent_id')
    prompt = data.get('prompt')

    if not agent_id or not prompt:
        return jsonify({'error': 'Agent ID and prompt are required'}), 400

    try:
        result = agent_service.generate_post(agent_id, prompt)

        # Trigger agents to react to posts
        agent_service.read_posts_and_act()

        return jsonify(result), 201
    except Exception as e:
        print(f"Error creating post: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/actions', methods=['GET'])
def get_actions():
    """
    Endpoint to get all actions performed by agents.
    """
    actions = session.query(AgentAction).all()
    action_list = []
    for action in actions:
        action_list.append({
            'agent_name': action.agent.name,
            'action_name': action.action.action,  # Corrected this line
            'target_agent_name': action.target_agent.name if action.target_agent else None,
            'post_id': action.post_id
        })
    return jsonify(action_list)

@app.route('/api/action_summary', methods=['GET'])
def get_action_summary():
    """
    Endpoint to get a summary of actions performed by agents, showing how many times each action
    was used by an agent against another agent.
    """
    # Create an alias for the Agent model to use it as the target agent
    TargetAgent = aliased(Agent)

    summary = (
        session.query(
            Agent.name.label('agent_name'),
            Action.action.label('action_name'),
            TargetAgent.name.label('target_agent_name'),
            func.count(AgentAction.id).label('action_count')
        )
        .join(Action, AgentAction.action_id == Action.id)
        .join(Agent, AgentAction.agent_id == Agent.id)
        .join(TargetAgent, AgentAction.target_agent_id == TargetAgent.id)
        .group_by(
            Agent.name,
            Action.action,
            TargetAgent.name
        )
        .all()
    )

    result = []
    for record in summary:
        result.append({
            'agent_name': record.agent_name,
            'action_name': record.action_name,
            'target_agent_name': record.target_agent_name,
            'action_count': record.action_count
        })
    return jsonify(result)


@app.route('/agents', methods=['GET'])
def list_agents():
    """
    Endpoint to list all created agents.
    """
    agents = agent_service.get_agents()
    return jsonify(agents), 200

@app.route('/agent/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    """
    Endpoint to get details of a specific agent by ID.
    """
    agent = agent_service.get_agent_by_id(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    return jsonify(agent), 200

@app.route('/interact', methods=['POST'])
def interact():
    """
    Endpoint to simulate an interaction between agents.
    Expects a JSON payload with 'agent_name', 'interaction_type', and 'content'.
    """
    data = request.json
    agent_name = data.get('agent_name')
    interaction_type = data.get('interaction_type')
    content = data.get('content')

    if not agent_name or not interaction_type or not content:
        return jsonify({'error': 'Agent name, interaction type, and content are required'}), 400

    interaction_result = agent_service.interact(agent_name, interaction_type, content)

    # Here you would save the interaction to the database, for example:
    # interaction = Interaction(agent_id=agent.id, interaction_type=interaction_type, content=interaction_result)
    # session.add(interaction)
    # session.commit()

    return jsonify({'interaction': interaction_result}), 201

# API routes for frontend
@app.route('/api/agents', methods=['GET'])
def api_get_agents():
    agents = agent_service.get_agents()
    return jsonify(agents)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        conn.close()

        # Debugging output to see the raw posts data
        print(f"Fetched posts: {posts}")

        # Format the result for JSON response
        post_list = [{'id': post[0], 'agent_id': post[1], 'content': post[2], 'prompt': post[3], 'timestamp': post[4]}
                     for post in posts]

        # Debugging output to see the formatted post list
        print(f"Formatted post list: {post_list}")

        return jsonify(post_list)
    except Exception as e:
        # Log the specific error to the console
        print(f"Error fetching posts: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=Config.DEBUG)
