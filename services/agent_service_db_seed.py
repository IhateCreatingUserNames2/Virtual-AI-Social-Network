import sys
import os
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.database_models.models import Action
from config.config import Config
import csv

# Path to your SQLite database file and CSV file
db_path = 'E:/ProjetosPython/NEWAI/app.db'
csv_path = 'E:/ProjetosPython/NEWAI/data/actions.csv'

# Database setup using SQLAlchemy
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()

# Function to check for existing tables
def check_tables(engine):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result]
        return tables

# Check if the necessary table exists
required_tables = ['actions']
existing_tables = check_tables(engine)
missing_tables = [table for table in required_tables if table not in existing_tables]

if missing_tables:
    print(f"Missing tables: {', '.join(missing_tables)}")
    sys.exit(1)

print("All required tables are present.")

# Function to seed the actions into the database
def seed_actions():
    """
    Populate the Action table in the database with data loaded from the CSV file.
    """
    try:
        with open(csv_path, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Processing row: {row}")  # Debugging line to print each row
                # Create a new Action object
                action = Action(
                    personality_type=row['Personality'],
                    action=row['Action'],
                    probability_level=row['Probability']
                )
                # Add the action to the session
                session.add(action)
        # Commit the session to write the actions to the database
        session.commit()
        print("Actions seeded successfully!")
    except FileNotFoundError:
        print(f"The CSV file at {csv_path} was not found.")
    except KeyError as e:
        print(f"CSV file is missing required columns: {e}")
    except UnicodeDecodeError as e:
        print(f"Error reading CSV file: {e}")
    except Exception as e:
        print(f"An error occurred while seeding actions: {e}")
    finally:
        session.close()

# Run the seeding function
if __name__ == '__main__':
    seed_actions()
