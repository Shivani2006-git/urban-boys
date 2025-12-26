from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'urban_boys_secret_key_change_this_later'

# 1. Database connection - SQLite (Local File)
DB_NAME = "database.db"

def get_db_connection():
    try:
        # check_same_thread=False is needed for Flask
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        return conn
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

# Initialize tables
def init_db():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # Products Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    description TEXT,
                    image_url VARCHAR(500)
                )
            """)
            
            # Users Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
            
            # Admins Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
            
            # Check if default admin exists
            cursor.execute("SELECT * FROM admins WHERE username = 'admin'")
            if not cursor.fetchone():
                cursor.execute("INSERT INTO admins (username, password) VALUES ('admin', 'admin123')")
                print("✅ Default admin user created (admin/admin123)")
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Tables checked/created!")
    except Exception as e:
        print(f"❌ Initialization Error: {e}")

# Run init on startup
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save-user', methods=['POST'])
def save_user():
    user = request.form.get('username')
    passw = request.form.get('password')
    
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Connection returned None")
    except Exception as e:
        return f"❌ Database Connection Error: {str(e)}"
    
    try:
        cursor = conn.cursor() 
        # SQLite uses ? for placeholders
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, passw))
        conn.commit()
        cursor.close()
        conn.close() 
    except Exception as e:
        if "UNIQUE constraint failed" in str(e) or "duplicate" in str(e).lower():
            return render_template('index.html', error_msg="Username already taken!")
        return render_template('index.html', error_msg=f"Error: {e}")
    
    # SUCCESS: Redirect to dashboard
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def login():
    user_val = request.form.get('username')
    pass_val = request.form.get('password')
    
    conn = get_db_connection()
    if conn is None:
        return "❌ Database Connection Failed."

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user_val, pass_val))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        return render_template('index.html', error_msg="Login failed due to system error.")
    
    if user:
        # Fetch products for the dashboard
        products = []
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, price, image_url FROM products ORDER BY id DESC")
                products = cursor.fetchall()
                cursor.close()
                conn.close()
        except Exception as e:
            print(f"Error fetching products: {e}")

        # This sends the user to your shop after successful login
        return render_template('dashboard.html', username=user_val, products=products)
    else:
        return render_template('index.html', error_msg="Invalid credentials. Try again!")

@app.route('/dashboard')
@app.route('/dashboard')
def dashboard():
    # Fetch products for the dashboard
    products = []
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, image_url FROM products ORDER BY id DESC")
            products = cursor.fetchall()
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error fetching products: {e}")
        
    return render_template('dashboard.html', products=products)

# --- ADMIN ROUTES ---

@app.route('/admin-login')
def admin_login_page():
    return render_template('admin_login.html')

@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
            admin = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if admin:
                session['is_admin'] = True
                return redirect(url_for('admin'))
            else:
                return "❌ Invalid Admin Credentials. <a href='/admin-login'>Try again</a>"
        except Exception as e:
            return f"Error: {e}"
    return "DB Connection Failed"

@app.route('/admin-logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login_page'))
        
    # Fetch products to show the list for deletion
    products = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price, image_url FROM products ORDER BY id DESC")
            products = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception:
            pass
            
    return render_template('admin.html', products=products)

@app.route('/delete-product/<int:product_id>')
def delete_product(product_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login_page'))
        
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Product {product_id} deleted.")
        except Exception as e:
            print(f"❌ Error deleting product: {e}")
            
    return redirect(url_for('admin'))

@app.route('/add-product', methods=['POST'])
def add_product():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login_page'))
        
    name = request.form.get('name')
    price = request.form.get('price')
    image_url = request.form.get('image_url')
    description = request.form.get('description')
    
    try:
        conn = get_db_connection()
        if conn is None:
            print("❌ Database Connection Failed when adding product.")
            return redirect(url_for('admin'))

        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, image_url, description) VALUES (?, ?, ?, ?)", 
                       (name, price, image_url, description))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Product '{name}' added successfully!")
    except Exception as e:
        print(f"❌ Error adding product: {e}")
        
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
