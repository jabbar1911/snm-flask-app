# 🚀 Smart Note Management (SNM) - Supabase Edition

A premium, secure personal workspace for managing notes and documents. This version is powered by **Supabase** (Auth, PostgreSQL, and Storage), featuring a cinematic glassmorphism UI and industrial-strength security.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![Supabase](https://img.shields.io/badge/Supabase-BaaS-orange)
![License](https://img.shields.io/badge/License-MIT-red)

---

## ✨ Features

### 🔐 Multi-Factor Security (Supabase Auth)
- **Email Confirmation**: Automatic email verification for all new users.
- **Numeric OTP**: 6-digit access code verification for high-security registration.
- **Session Protection**: Encrypted server-side sessions.

### 📝 Intelligence Module (Notes)
- **Full CRUD**: Create, view, update, and delete personal notes.
- **PostgreSQL Power**: Fast, relational data management.
- **Excel Export**: Download all your notes as `.xlsx` files instantly.
- **Smart Search**: Case-insensitive keyword search across all notes.

### 🛡️ Asset Vault (Storage)
- **Optimized Storage**: Files are stored in **Supabase Buckets** (not the database), ensuring high performance.
- **Up to 16MB**: Support for larger documents, PDFs, and images.
- **Secure Links**: Temporary secure download and preview links.

### 🗑️ Data Privacy
- **Total Deletion**: Delete individual notes/files or your entire account with one click (GDPR compliant).

---

## 🛠️ Technology Stack

- **Backend**: Python 13 + Flask 3.x
- **Infrastructure**: Supabase (BaaS)
  - **Database**: PostgreSQL
  - **Auth**: Managed Authentication
  - **Storage**: S3-compatible Buckets
- **Frontend**: Vanilla CSS3 (Glassmorphism), JavaScript, Jinja2
- **Data**: Flask-Excel (OpenPyXL)

---

## 📦 Installation & Setup

### 1. Supabase Configuration
1.  Go to [Supabase.com](https://supabase.com) and create a new project.
2.  **SQL Setup**: Run the SQL in `snm_schema.sql` (if available) or create these tables: `profiles`, `notesdata`, `filesdata`.
3.  **Storage Setup**: Create a **Public** bucket named **`files`**.
4.  **Security**: Enable RLS (Row Level Security) on all tables.

### 2. Local Setup
1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/jabbar1911/snm-flask-app
    cd snm-flask-app
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment**:
    Create a `.env` file:
    ```env
    # Supabase Credentials
    SUPABASE_URL=https://your-project.supabase.co
    SUPABASE_KEY=your-service-role-key
    
    # Flask Secret
    SECRET_KEY=any-random-string
    ```

### 3. Run Locally
```bash
python app.py
```

---

## 🚀 Deployment (Render)

1.  Connect your GitHub repo to **Render.com**.
2.  Set the **Build Command**: `pip install -r requirements.txt`.
3.  Set the **Start Command**: `gunicorn app:app`.
4.  Add your **Environment Variables** (SUPABASE_URL, SUPABASE_KEY, SECRET_KEY) in the Render dashboard.

---

## 📁 Clean Architecture
I have streamlined the project by removing unnecessary scripts. The app now handles everything through the `supabase` python client:
- ✅ `app.py` (Core Logic)
- ❌ `cmail.py` (Handled by Supabase)
- ❌ `otp.py` (Handled by Supabase)
- ❌ `stoken.py` (Handled by Supabase)
- ❌ `snm_schema.sql` (Migrated to Cloud)

---

## 🎓 Interview Talking Points
- **Architecture**: "I migrated from MySQL to a Cloud-Native BaaS (Supabase) to improve scalability and security."
- **Storage Strategy**: "I implemented cloud-bucket storage for files instead of database BLOBs, allowing for 16MB uploads without slowing down the database."
- **Security**: "I used Row Level Security (RLS) policies to ensure users can only ever access their own data at the database layer."

---

⭐ **Made with ❤️ by SNM Systems**
⭐ **If you find this useful, give it a star!**
