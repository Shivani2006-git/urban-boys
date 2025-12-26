# 🚀 Publishing Your Website (Ready to Deploy!)

I have already initialized the Git repository and committed all your files for you. ✅

---

### **Step 1: Create a GitHub Repository**
1. Log in to [GitHub.com](https://github.com).
2. Click the **+** icon (top right) -> **New repository**.
3. Name it: `urban-boys`
4. Set it to **Public** (or Private).
5. Click **Create repository**.

### **Step 2: Connect Code to GitHub**
Copy the commands GitHub shows you under **"…or push an existing repository from the command line"**, or simply run these two commands in your terminal:

```bash
git remote add origin https://github.com/YOUR_USERNAME/urban-boys.git
git push -u origin master
```
*(Replace `YOUR_USERNAME` with your actual GitHub username)*

---

### **Step 3: Deploy on Render.com (Simple & Free)**
1. Sign up on [Render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Select your new `urban-boys` repository.
4. Use these exact settings:
   - **Name:** `urban-boys-shop`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

5. Click **Create Web Service**.

**Wait 2 minutes, and your site will be live! 🌍**
