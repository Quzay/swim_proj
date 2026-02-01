from sqlalchemy import text
from database import engine 

def check_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT current_user, current_database();"))
            user, db = result.fetchone()
            print(f" Success! Connected to '{db}' as user '{user}'")
            
    except Exception as e:
        print(f"Connection failed!")
        print(f"Error details: {e}")

if __name__ == "__main__":
    check_connection()