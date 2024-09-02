-- Table for storing agent profiles
CREATE TABLE agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    personality_type VARCHAR(10) NOT NULL,
    profile TEXT NOT NULL,
    tuning TEXT NOT NULL  -- Add this column
);

-- Table for storing interactions between agents and/or posts
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INT REFERENCES agents(id),
    interaction_type VARCHAR(50),
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for logging the posts made by agents
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INT REFERENCES agents(id),
    prompt TEXT NOT NULL,                           -- Store the prompt made by the user
    content TEXT NOT NULL,                          -- Store the response generated by the LLM
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes INT DEFAULT 0,
    comments_count INT DEFAULT 0
);

-- Table for logging comments made on posts
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INT REFERENCES posts(id),
    agent_id INT REFERENCES agents(id),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing relationships between agents (e.g., friends, followers)
CREATE TABLE agent_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INT REFERENCES agents(id),
    related_agent_id INT REFERENCES agents(id),
    relationship_type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing personality types with prompts and tuning
CREATE TABLE personalities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personality_type VARCHAR(50) NOT NULL, -- e.g., "Narcisista"
    prompt TEXT NOT NULL,                  -- e.g., "Você é uma pessoa que se considera superior aos outros..."
    tuning JSON NOT NULL                   -- e.g., '{"confidence": "alta", "empathy": "baixa", "assertiveness": "alta"}'
);

-- Tabela para armazenar ações disponíveis para cada personalidade
CREATE TABLE actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personality_type VARCHAR(50) NOT NULL, -- Tipo de personalidade
    action VARCHAR(100) NOT NULL,           -- Nome da ação
    probability_level VARCHAR(10) NOT NULL  -- Nível de probabilidade: Baixo, Médio, Alto
);

-- Tabela para registrar as ações realizadas pelos agentes
CREATE TABLE agent_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INT REFERENCES agents(id),
    action_id INT REFERENCES actions(id),
    target_agent_id INT REFERENCES agents(id), -- Agente alvo (se houver)
    post_id INT REFERENCES posts(id),          -- Post relacionado (se houver)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
