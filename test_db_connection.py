import psycopg2
from urllib.parse import quote_plus

# Credentials from app.py
raw_password = "#K9W5tSe#w$yZc&"
encoded_password = quote_plus(raw_password)
DB_URI = f"postgresql://postgres:{encoded_password}@db.gzgmaclzucnifunkkkgl.supabase.co:5432/postgres"

print(f"Attempting to connect to: {DB_URI}")

try:
    conn = psycopg2.connect(DB_URI)
    print("✅ Connection Successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection Failed: {e}")
