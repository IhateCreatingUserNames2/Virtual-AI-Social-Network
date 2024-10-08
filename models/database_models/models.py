# ORM models
# models/database_models/models.py
from sqlalchemy import (Column, Integer, String, Text, ForeignKey, DateTime, JSON)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    personality_type = Column(String(10), nullable=False)
    profile = Column(Text, nullable=False)
    profile_picture = Column(String)  # New field for profile picture path
    tuning = Column(JSON, nullable=False)  # Store tuning parameters as JSON

    # Relationships
    posts = relationship("Post", back_populates="agent")
    comments = relationship("Comment", back_populates="agent")
    interactions = relationship("Interaction", back_populates="agent")
    relationships = relationship("AgentRelationship",
                                  foreign_keys="[AgentRelationship.agent_id]",
                                  back_populates="agent")
    related_relationships = relationship("AgentRelationship",
                                          foreign_keys="[AgentRelationship.related_agent_id]",
                                          back_populates="related_agent")
    actions_performed = relationship("AgentAction", foreign_keys="[AgentAction.agent_id]", back_populates="agent")
    actions_received = relationship("AgentAction", foreign_keys="[AgentAction.target_agent_id]",
                                    back_populates="target_agent")

    def __repr__(self):
        return f"<Agent(name={self.name}, personality_type={self.personality_type}, tuning={self.tuning})>"

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    prompt = Column(Text, nullable=False)  # Store the prompt made by the user
    content = Column(Text, nullable=False)  # Store the response generated by the LLM
    timestamp = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    # Relationships
    agent = relationship("Agent", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    related_actions = relationship("AgentAction", back_populates="post")

    def __repr__(self):
        return f"<Post(agent_id={self.agent_id}, content={self.content[:20]}...)>"

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    post = relationship("Post", back_populates="comments")
    agent = relationship("Agent", back_populates="comments")

    def __repr__(self):
        return f"<Comment(post_id={self.post_id}, agent_id={self.agent_id}, content={self.content[:20]}...)>"

class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    personality_type = Column(String(50), nullable=False)  # Tipo de personalidade
    action = Column(String(100), nullable=False)           # Nome da ação
    probability_level = Column(String(10), nullable=False) # Nível de probabilidade

    # Relacionamentos
    agent_actions = relationship("AgentAction", back_populates="action")

    def __repr__(self):
        return f"<Action(personality_type={self.personality_type}, action={self.action}, probability_level={self.probability_level})>"

class AgentAction(Base):
    __tablename__ = 'agent_actions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    action_id = Column(Integer, ForeignKey('actions.id'), nullable=False)
    target_agent_id = Column(Integer, ForeignKey('agents.id'), nullable=True)  # Agente alvo (se houver)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=True)            # Post relacionado (se houver)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    agent = relationship("Agent", foreign_keys=[agent_id], back_populates="actions_performed")
    action = relationship("Action", back_populates="agent_actions")
    target_agent = relationship("Agent", foreign_keys=[target_agent_id], back_populates="actions_received")
    post = relationship("Post", back_populates="related_actions")

    def __repr__(self):
        return f"<AgentAction(agent_id={self.agent_id}, action_id={self.action_id}, target_agent_id={self.target_agent_id}, post_id={self.post_id})>"


class Interaction(Base):
    __tablename__ = 'interactions'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    interaction_type = Column(String(50))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("Agent", back_populates="interactions")

    def __repr__(self):
        return f"<Interaction(agent_id={self.agent_id}, type={self.interaction_type})>"

class AgentRelationship(Base):
    __tablename__ = 'agent_relationships'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    related_agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    relationship_type = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("Agent", foreign_keys=[agent_id], back_populates="relationships")
    related_agent = relationship("Agent", foreign_keys=[related_agent_id], back_populates="related_relationships")

    def __repr__(self):
        return f"<AgentRelationship(agent_id={self.agent_id}, related_agent_id={self.related_agent_id}, type={self.relationship_type})>"

class Personality(Base):
    __tablename__ = 'personalities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    personality_type = Column(String(50), nullable=False)  # e.g., "Narcisista"
    prompt = Column(Text, nullable=False)  # e.g., "Você é uma pessoa que se considera superior aos outros..."
    tuning = Column(JSON, nullable=False)  # Store tuning parameters as JSON

    def __repr__(self):
        return f"<Personality(personality_type={self.personality_type}, prompt={self.prompt[:20]}...)>"
