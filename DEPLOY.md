# 🚀 Publishing Your Website

You can choose between **Render** (Recommended for this app) or **PythonAnywhere**.

---

## 🟢 Option 1: Render.com (Recommended for Free Tier)
**Why?** It allows connections to your Supabase database for free.

### **Step 1: Push to GitHub**
1. Create a repo on GitHub (e.g., `urban-boys`).
2. Upload `app.py`, `requirements.txt`, `Procfile`, and `templates/` folder.

### **Step 2: Deploy**
1. Sign up on [Render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repo.
4. Settings:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Deploy**.

---

## 🔵 Option 2: PythonAnywhere
**Note:** The **Free** plan blocks external database connections (Supabase). You need the **$5/month** plan to use your current database.

### **Step 1: Setup**
1. Create a zip file of your project folder.
2. Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com).
3. Go to **Files** tab -> Upload your zip -> Unzip it properly.

### **Step 2: Configuration**
1. Go to **Web** tab -> **Add a new web app**.
2. Select **Flask** -> **Python 3.9+**.
3. Path to your code: Enter the path where you uploaded files (e.g., `/home/yourusername/mysite/app.py`).

### **Step 3: Dependencies**
1. Open a **Bash Console**.
2. Run: 
   ```bash
   pip3 install --user flask psycopg2-binary
   ```

### **Step 4: WSGI Configuration**
1. In the **Web** tab, click the link to edit the **WSGI configuration file**.
2. It will open an editor. Delete everything and paste this:
   ```python
   import sys
   import os

   # Add your project directory to the sys.path
   project_home = '/home/YOUR_USERNAME/mysite'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path

   # Import flask app but need to call it "application" for WSGI to work
   from app import app as application
   ```
   *(Replace `YOUR_USERNAME` and paths accordingly)*.

3. **Save** and **Reload** the web app.

---
### ⚠️ Crucial Note for PythonAnywhere Free Users
If you get a "Connection Error" to the database, it is because PythonAnywhere Free Tier blocks port 5432 (Postgres). You must either:
1. Upgrade to the **Hacker Plan ($5)**.
2. OR: Switch to using PythonAnywhere's internal MySQL database (requires changing `app.py` code).
