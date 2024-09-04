import sqlite3

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'

# Dictionary mapping Agent_ID to a generated name based on their personality
agent_names = {
    21: "Victoria",  # Agent_1 - Narcisista
    22: "Elena",     # Agent_2 - Empático
    23: "Dante",     # Agent_3 - Antissocial
    24: "Vincent",   # Agent_4 - Obsessivo-compulsivo
    25: "Marcus",    # Agent_5 - Paranoico
    26: "Lucas",     # Agent_6 - Dependente
    27: "Isabella",  # Agent_7 - Histriônico
    28: "Sophia",    # Agent_8 - Borderline
    29: "Aurora",    # Agent_9 - Esquizotípico
    30: "Gabriel",  # Agent_10 - Passivo-agressivo
    31: "Maria",    # Agent_11 - Altruísta
    32: "Clara",    # Agent_12 - Perfeccionista
    33: "Amelia",   # Agent_13 - Sociável
    34: "Luna",     # Agent_14 - Melancólico
    35: "Hope",     # Agent_15 - Resiliente
    36: "Alice",    # Agent_16 - Impulsivo
    37: "Nina",     # Agent_17 - Introvertido
    38: "Noah",     # Agent_18 - Fóbico
    39: "Oliver",   # Agent_19 - Ansioso
    40: "Joy",      # Agent_20 - Optimista
}

def update_agent_names():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Update the agents table with the new names
    for agent_id, name in agent_names.items():
        cursor.execute("UPDATE agents SET name = ? WHERE id = ?", (name, agent_id))
        conn.commit()

    # Close the connection
    conn.close()
    print("Agent names updated successfully.")

if __name__ == "__main__":
    update_agent_names()
