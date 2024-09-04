from sqlalchemy import create_engine, inspect

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'
engine = create_engine(f"sqlite:///{db_path}")

# Create an inspector to introspect the database
inspector = inspect(engine)

# Get all table names
tables = inspector.get_table_names()

# Iterate through each table and print its columns
for table_name in tables:
    print(f"\nTable: {table_name}")
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(f"  Column: {column['name']}, Type: {column['type']}, Nullable: {column['nullable']}")

# Close the engine
engine.dispose()
