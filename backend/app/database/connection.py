
import sqlite3
from pathlib import Path
from contextlib import contextmanager

# Backend directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database directory
DATABASE_DIR = BASE_DIR / "data"

# Create directory if it doesn't exist
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# Database file path
DATABASE_PATH = DATABASE_DIR / "reviews.db"


def get_connection():
    """
    Creates and returns a SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    return connection


@contextmanager
def db_connection():
    """
    Provides a database connection with
    automatic commit, rollback and closing.
    """

    connection = get_connection()

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def initialize_database():
    """
    Creates all required database tables.
    """

    with db_connection() as connection:

        connection.executescript("""
        
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repository_name TEXT NOT NULL,
            diff_text TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            recommendation TEXT,
            summary TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );


        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id INTEGER NOT NULL,
            agent_name TEXT NOT NULL,
            file_path TEXT,
            line_number INTEGER,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            suggestion TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (review_id)
                REFERENCES reviews(id)
                ON DELETE CASCADE
        );


        CREATE TABLE IF NOT EXISTS agent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id INTEGER NOT NULL,
            agent_name TEXT NOT NULL,
            status TEXT NOT NULL,
            output TEXT,
            started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME,

            FOREIGN KEY (review_id)
                REFERENCES reviews(id)
                ON DELETE CASCADE
        );

        """)

    print("SQLite database initialized successfully!")
