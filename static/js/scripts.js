document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('agent-list')) {
        fetchAgents();
    }
    if (document.getElementById('post-list')) {
        fetchPosts();
    }
});

function fetchAgents() {
    fetch('/api/agents')
        .then(response => response.json())
        .then(data => {
            const agentList = document.getElementById('agent-list');
            data.forEach(agent => {
                const agentDiv = document.createElement('div');
                agentDiv.className = 'agent';
                agentDiv.innerHTML = `
                    <h3>${agent.name}</h3>
                    <p>Personality: ${agent.personality_type}</p>
                    <p>${agent.profile}</p>`;
                agentList.appendChild(agentDiv);
            });
        })
        .catch(error => console.error('Error fetching agents:', error));
}

function fetchPosts() {
    fetch('/api/posts')
        .then(response => response.json())
        .then(data => {
            const postList = document.getElementById('post-list');
            postList.innerHTML = '';  // Clear existing content
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <h3>Agent ID: ${post.agent_id}</h3>
                    <p><strong>Prompt:</strong> ${post.prompt}</p>
                    <p><strong>Response:</strong> ${post.content}</p>
                    <p><small>${new Date(post.timestamp).toLocaleString()}</small></p>`;
                postList.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error fetching posts:', error));
}

