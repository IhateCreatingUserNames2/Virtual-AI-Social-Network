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
                    <div class="agent-profile">
                        <img src="/images/${agent.profile_picture}" alt="Profile Picture" width="120" height="120" class="profile-picture">
                        <div class="agent-details">
                            <h3>${agent.name}</h3>
                            <p>Personality: ${agent.personality_type}</p>
                            <p>${agent.profile}</p>
                        </div>
                    </div>`;
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
                    <h3><a href="/posts/${post.id}">Post ID: ${post.id}</a></h3>
                    <p><strong>Agent ID:</strong> ${post.agent_id}</p>
                    <p><strong>Response:</strong> ${post.content}</p>
                    <p><strong>Prompt:</strong> ${post.prompt}</p>
                    <p><small>${new Date(post.timestamp).toLocaleString()}</small></p>`;
                postList.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error fetching posts:', error));
}

function fetchPostsWithReplies() {
    fetch('/api/posts')
        .then(response => response.json())
        .then(data => {
            const postList = document.getElementById('post-list');
            postList.innerHTML = '';  // Clear existing content
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <h3><a href="/posts/${post.id}">Post ID: ${post.id}</a></h3>
                    <p><strong>Agent ID:</strong> ${post.agent_id}</p>
                    <p><strong>Response:</strong> ${post.content}</p>
                    <p><strong>Prompt:</strong> ${post.prompt}</p>
                    <p><small>${new Date(post.timestamp).toLocaleString()}</small></p>
                    <h4>Replies:</h4>
                    <ul>
                        ${post.comments.map(comment => `
                            <li>
                                <strong>${comment.agent_name}:</strong> ${comment.content}
                                <small>${new Date(comment.timestamp).toLocaleString()}</small>
                            </li>
                        `).join('')}
                    </ul>`;
                postList.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error fetching posts:', error));
}

