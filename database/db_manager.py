import pg8000.dbapi
import config

def get_connection():
    """Создает и возвращает подключение к базе данных PostgreSQL (через pg8000)."""
    return pg8000.dbapi.connect(
        database=config.DB_NAME,  # Обрати внимание, тут database вместо dbname
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=int(config.DB_PORT)  # Порт обязательно должен быть целым числом
    )


def init_db():
    """Initializes the database and creates required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table (using BIGINT for Telegram user IDs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username VARCHAR(255),
            reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tasks table with ON DELETE CASCADE for data integrity
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            task_text TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

def add_user(user_id, username):
    """Registers a new user if they don't exist."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (user_id, username) 
            VALUES (%s, %s) 
            ON CONFLICT (user_id) DO NOTHING
        ''', (user_id, username))
        conn.commit()
    except Exception as e:
        print(f"Database error while adding user: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def add_task(user_id, task_text):
    """Adds a new task to the user's to-do list."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (user_id, task_text) VALUES (%s, %s)", (user_id, task_text))
        conn.commit()
    except Exception as e:
        print(f"Database error while adding task: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def get_tasks(user_id):
    """Retrieves all tasks for a specific user."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT task_text FROM tasks WHERE user_id = %s", (user_id,))
        tasks = cursor.fetchall()
        return [t[0] for t in tasks]
    except Exception as e:
        print(f"Database error while fetching tasks: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def clear_tasks(user_id):
    """Deletes all tasks for a specific user."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE user_id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Database error while clearing tasks: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()