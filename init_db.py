import psycopg2
from urllib.parse import quote_plus

# Database connection setup
raw_password = "#K9W5tSe#w$yZc&"
encoded_password = quote_plus(raw_password)
DB_URI = f"postgresql://postgres:{encoded_password}@db.gzgmaclzucnifunkkkgl.supabase.co:5432/postgres"

def init_db():
    try:
        conn = psycopg2.connect(DB_URI)
        cursor = conn.cursor()
        
        print("Connected to database...")

        # 1. Create Admins Table
        print("Creating 'admins' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # 2. Check/Add Default Admin
        cursor.execute("SELECT * FROM admins WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO admins (username, password) VALUES ('admin', 'admin123')")
            print("Default admin user 'admin' created.")
        else:
            print("Default admin user already exists.")

        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialization complete! You can now login.")
        
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()
