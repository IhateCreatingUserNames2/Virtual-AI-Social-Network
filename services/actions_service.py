from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.config import Config
from models.database_models.models import Action  # Assuming Action model is defined here

class ActionsService:
    def __init__(self, actions_data):
        self.actions_data = actions_data
        self.actions = self.load_actions()

        # Database setup
        engine = create_engine(Config.DATABASE_URI)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def load_actions(self):
        """
        Load actions from the provided data.
        """
        actions = []
        for action_row in self.actions_data:
            action = Action(
                personality_type=action_row['personality_type'],
                action_name=action_row['action'],
                probability=action_row['probability']
            )
            actions.append(action)
        return actions

    def seed_actions(self):
        """
        Populate the actions table in the database with the loaded actions.
        """
        for action in self.actions:
            self.session.add(action)
        self.session.commit()
        print("Actions seeded successfully!")

    def get_actions(self):
        """
        Retrieve all actions from the database.
        """
        return self.session.query(Action).all()

    def get_actions_by_personality(self, personality_type):
        """
        Retrieve actions by personality type.
        """
        return self.session.query(Action).filter_by(personality_type=personality_type).all()
