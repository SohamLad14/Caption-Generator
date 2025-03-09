import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS captions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT UNIQUE,
            caption TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Insert a new caption
def insert_caption(file_name, caption):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO captions (file_name, caption) VALUES (?, ?)", (file_name, caption))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Caption for {file_name} already exists.")
    conn.close()

# Retrieve a caption
def get_caption(file_name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT caption FROM captions WHERE file_name = ?", (file_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
