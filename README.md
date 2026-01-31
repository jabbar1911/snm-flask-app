# 🚀 Smart Note Management (SNM)

A secure and elegant personal workspace for managing notes and documents with OTP-based authentication and a modern glassmorphism interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange)
![License](https://img.shields.io/badge/License-Educational-red)

## ✨ What is SNM?

SNM is a full-stack web application that provides a secure, personal workspace where users can:
- Capture and organize their thoughts in notes
- Store confidential documents in an encrypted vault
- Search across all content instantly
- Export data to Excel for backup or analysis

Built with Flask and powered by Aiven's cloud MySQL database, SNM emphasizes security with OTP email verification and session management, while delivering a premium user experience through a responsive glassmorphism UI.

## 🎯 Key Features

### 🔐 Secure Authentication
- **OTP Verification**: Email-based one-time password for registration
- **Session Management**: Secure server-side sessions with auto-expiry
- **Password Protection**: Industry-standard password hashing

### 📝 Intelligence Module (Notes)
- Create, edit, and delete notes with rich text support
- Automatic timestamps for creation and updates
- Export all notes to Excel (.xlsx) format
- Full-text search across all your notes

### 🛡️ Asset Vault (Files)
- Upload and store documents securely in the database (as LONGBLOB)
- Supported formats: PDF, DOC, DOCX, TXT, PNG, JPG, JPEG, GIF
- Download files anytime with secure links
- Maximum file size: 10MB per upload

### 🔍 Global Search
- Search notes by title or content
- Find files by filename
- Instant results with keyword highlighting

### 🗑️ Account Control
- Update profile information
- Complete account deletion with full data removal (GDPR compliant)

## 🛠️ Technology Stack

**Backend:**
- Python 3.8+
- Flask (Web Framework)
- MySQL 8.0+ via Aiven (Cloud Database)
- Brevo API (Email Service)

**Frontend:**
- HTML5 & CSS3
- Bootstrap 5 (Responsive Design)
- Vanilla JavaScript
- Custom Glassmorphism Styling

**Additional Libraries:**
- Flask-Session (Session Management)
- Flask-Excel (Excel Export)
- mysql-connector-python (Database Driver)
- Gunicorn (Production Server)

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Aiven account with MySQL database ([Sign up free](https://aiven.io))
- Brevo account ([Sign up free](https://www.brevo.com))

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/jabbar1911/snm-flask-app
cd snm-flask-app
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Aiven MySQL database**

- Go to [Aiven Console](https://console.aiven.io)
- Create a new MySQL service (free tier available)
- Wait for the service to start (takes 2-3 minutes)
- Click on your service → **Overview** tab
- Download CA certificate (for secure connection)
- Note down connection details:
  - Host (e.g., `mysql-xxxxx.aivencloud.com`)
  - Port (usually `12345`)
  - Username (default: `avnadmin`)
  - Password (auto-generated)
  - Database name (default: `defaultdb`)

**Import database schema:**
```bash
# Using MySQL client with SSL
mysql --host=your-aiven-host \
      --port=your-port \
      --user=avnadmin \
      --password=your-password \
      --ssl-ca=ca.pem \
      defaultdb < snm_schema.sql
```

Or use Aiven's web console to run the SQL script directly:
1. Log in to [Aiven Console](https://console.aiven.io).
2. Go to your MySQL service → **Query Editor**.
3. Copy the contents of `snm_schema.sql` and paste it there.
4. Click **Run**.

5. **Configure environment variables**

Create a `.env` file in the project root:
```env
# Aiven MySQL Configuration
DB_HOST=mysql-xxxxx.aivencloud.com
DB_PORT=12345
DB_USERNAME=avnadmin
DB_PASSWORD=your_aiven_password
DB_NAME=defaultdb

# Brevo Email Configuration
BREVO_API_KEY=your_brevo_api_key
SENDER_EMAIL=your_verified_email@domain.com

# Flask Configuration
SECRET_KEY=your_random_secret_key
FLASK_ENV=development
```

**Generate a SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

6. **Get Brevo API credentials**
- Visit [Brevo.com](https://www.brevo.com) and create account
- Go to Settings → SMTP & API → Create API Key
- Verify your sender email address
- Add credentials to `.env`

7. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🚀 Deployment (Render)

**Note:** Since you're using Aiven for the database, your database is already cloud-hosted and will work seamlessly with Render deployment. No additional database setup needed!

### Prepare for Deployment

1. **Create required files**

`runtime.txt`:
```
python-3.11.0
```

`Procfile`:
```
web: gunicorn app:app
```

`.gitignore`:
```
venv/
__pycache__/
*.pyc
.env
flask_session/
```

2. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Deploy on Render

1. Go to [Render.com](https://render.com) and sign in
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: smart-note-management
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. Add environment variables (same as `.env` but with production values)
6. Click **Create Web Service**

Your app will be live at `https://your-app-name.onrender.com`

## 📁 Project Structure

```
smart-note-management/
├── app.py                  # Main Flask application
├── cmail.py               # Brevo email integration
├── otp.py                 # OTP generation logic
├── stoken.py              # Secure token encryption
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version
├── Procfile              # Gunicorn config
├── .env                  # Environment variables (local only)
│
├── static/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   └── images/           # Images and icons
│
├── templates/
│   ├── index.html        # Landing page
│   ├── register.html     # Registration
│   ├── login.html        # Login
│   ├── dashboard.html    # Main dashboard
│   ├── notes.html        # Notes management
│   ├── vault.html        # File vault
│   └── search.html       # Search page
│
└── database/
    └── snm_schema.sql    # Database schema
```

## 📖 Usage Guide

### Getting Started

1. **Register**: Click "Sign Up" and enter your details
2. **Verify OTP**: Check your email for the verification code
3. **Login**: Access your dashboard with your credentials

### Managing Notes

- **Create**: Click "Intelligence" → "Add Note" → Enter title and content → Save
- **Edit**: Click the edit icon on any note → Modify → Update
- **Delete**: Click the delete icon → Confirm removal
- **Export**: Click "Export Notes" to download all notes as Excel

### Managing Files

- **Upload**: Go to "Asset Vault" → "Upload File" → Select file → Upload
- **Download**: Click download icon next to any file
- **Delete**: Click delete icon → Confirm permanent removal

### Search

- Use the search bar to find notes or files
- Results show matching notes and files instantly
- Click any result to view details

## 🔒 Security Features

- **OTP Authentication**: Email verification for new accounts
- **Password Hashing**: Secure password storage
- **Session Security**: Server-side sessions with HttpOnly cookies
- **SQL Injection Protection**: Prepared statements for all queries
- **File Validation**: Type and size checks on uploads
- **CSRF Protection**: Token-based form protection

## 🗄️ Database Schema

### Tables

**users**
- id, name, email, password, created_at, last_login

**notes**
- id, user_id, title, content, created_at, updated_at

**files**
- id, user_id, filename, file_data (LONGBLOB), file_type, file_size, uploaded_at

All tables use CASCADE delete to maintain referential integrity.

## 🐛 Troubleshooting

**Database Connection Error**
- Verify your Aiven service is running (check Aiven console)
- Check connection credentials in `.env`
- Ensure you're using the correct host and port
- Verify SSL certificate if required

**Email Not Sending**
- Verify Brevo API key is correct
- Check sender email is verified in Brevo dashboard

**File Upload Fails**
- Check file size (max 10MB)
- Verify file extension is allowed
- Contact Aiven support if database storage issues occur

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📝 License

This project is for **educational purposes only**. 

© 2026 SNM Systems. All Rights Reserved.

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/jabbar1911/snm-flask-app/issues)
- **Email**: 2100031733cser@gmail.com

---

⭐ If you find this project useful, please give it a star on GitHub!

**Made with ❤️ by SNM Systems**
